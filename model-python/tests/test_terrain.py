import unittest
import struct
import tempfile
import zlib
from pathlib import Path

from population_model.config import ModelConfig
from population_model.terrain import CellType, TerrainMap, load_terrain_map


TERRAIN_PATH = Path("Terrain maps/Terrain1.png")


class TerrainMapTests(unittest.TestCase):
    def setUp(self):
        self.config = ModelConfig(
            terrain_map_path=str(TERRAIN_PATH),
            restricted_cell_agent_ids=("agent-allowed",),
            exit_cell_agent_ids=("agent-exit",),
            gate_max_density=2,
            type_1_penalty_direction="north",
            type_1_penalty_multiplier=0.25,
        )
        self.terrain = load_terrain_map(self.config)

    def test_loads_selected_map_and_counts_cell_types(self):
        summary = self.terrain.summary()

        self.assertEqual(summary.width, 1213)
        self.assertEqual(summary.height, 839)
        self.assertEqual(summary.counts_by_type[CellType.NORMAL], 854869)
        self.assertEqual(summary.counts_by_type[CellType.TYPE_2_PENALTY], 106658)
        self.assertEqual(summary.counts_by_type[CellType.TYPE_1_PENALTY], 25578)
        self.assertEqual(summary.counts_by_type[CellType.BOUNDARY], 17586)
        self.assertEqual(summary.counts_by_type[CellType.DENSITY_ZERO], 3370)
        self.assertEqual(summary.counts_by_type[CellType.EXIT], 5684)
        self.assertEqual(summary.counts_by_type[CellType.RESTRICTED], 3125)
        self.assertEqual(summary.counts_by_type[CellType.GATE], 837)

    def test_initializes_representative_cells_from_map_legend(self):
        samples = self._first_cell_by_type()

        self.assertEqual(self.terrain.cell_at(*samples[CellType.NORMAL]).cell_type, CellType.NORMAL)
        self.assertEqual(
            self.terrain.cell_at(*samples[CellType.BOUNDARY]).cell_type,
            CellType.BOUNDARY,
        )

        restricted = self.terrain.cell_at(*samples[CellType.RESTRICTED])
        self.assertEqual(restricted.allowed_agent_ids, ("agent-allowed",))

        gate = self.terrain.cell_at(*samples[CellType.GATE])
        self.assertEqual(gate.max_density, 2)

        exit_cell = self.terrain.cell_at(*samples[CellType.EXIT])
        self.assertEqual(exit_cell.exit_agent_ids, ("agent-exit",))

        type_1 = self.terrain.cell_at(*samples[CellType.TYPE_1_PENALTY])
        self.assertIsNotNone(type_1.penalty)
        self.assertEqual(type_1.penalty.kind, "type_1")
        self.assertEqual(type_1.penalty.direction, "north")
        self.assertEqual(type_1.penalty.multiplier, 0.25)

        type_2 = self.terrain.cell_at(*samples[CellType.TYPE_2_PENALTY])
        self.assertIsNotNone(type_2.penalty)
        self.assertEqual(type_2.penalty.kind, "type_2")
        self.assertEqual(type_2.penalty.multiplier, 0.5)

    def test_traversability_rules_use_configured_cell_properties(self):
        samples = self._first_cell_by_type()

        self.assertFalse(
            self.terrain.is_traversable(*samples[CellType.BOUNDARY], agent_id="any")
        )
        self.assertFalse(
            self.terrain.is_traversable(
                *samples[CellType.RESTRICTED], agent_id="agent-blocked"
            )
        )
        self.assertTrue(
            self.terrain.is_traversable(
                *samples[CellType.RESTRICTED], agent_id="agent-allowed"
            )
        )
        self.assertTrue(
            self.terrain.is_traversable(
                *samples[CellType.GATE], agent_id="any", current_density=1
            )
        )
        self.assertFalse(
            self.terrain.is_traversable(
                *samples[CellType.GATE], agent_id="any", current_density=2
            )
        )
        self.assertTrue(
            self.terrain.is_exit_cell(*samples[CellType.EXIT], agent_id="agent-exit")
        )
        self.assertFalse(
            self.terrain.is_exit_cell(*samples[CellType.EXIT], agent_id="other")
        )

    def test_summary_serializes_for_future_snapshots(self):
        payload = self.terrain.to_dict()

        self.assertEqual(payload["source"], str(TERRAIN_PATH))
        self.assertEqual(payload["summary"]["width"], 1213)
        self.assertEqual(payload["legend"]["normal"], {"r": 255, "g": 255, "b": 255})
        self.assertEqual(payload["summary"]["counts_by_type"]["boundary"], 17586)
        self.assertEqual(payload["summary"]["counts_by_type"]["density_zero"], 3370)

    def _first_cell_by_type(self):
        samples = {}
        for index, cell_type in enumerate(self.terrain.cell_types):
            if cell_type not in samples:
                x = index % self.terrain.width
                y = index // self.terrain.width
                samples[cell_type] = (x, y)
        self.assertEqual(set(samples), set(CellType))
        return samples


class TerrainMapValidationTests(unittest.TestCase):
    def test_rejects_missing_map(self):
        with self.assertRaises(FileNotFoundError):
            TerrainMap.from_png("Terrain maps/not-here.png", ModelConfig())

    def test_brown_cells_are_density_zero_reflective_boundaries(self):
        path = self._write_png(
            [
                [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
                [(0, 0, 0), (185, 122, 87), (0, 0, 0)],
                [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
            ]
        )
        terrain = TerrainMap.from_png(path, ModelConfig())

        cell = terrain.cell_at(1, 1)

        self.assertEqual(cell.cell_type, CellType.DENSITY_ZERO)
        self.assertFalse(terrain.is_traversable(1, 1, agent_id="any"))
        self.assertEqual(
            terrain.summary().counts_by_type[CellType.DENSITY_ZERO], 1
        )

    def test_reports_cell_definitions_outside_black_outer_boundary(self):
        path = self._write_png(
            [
                [(255, 255, 255), (237, 28, 36), (255, 255, 255)],
                [(255, 255, 255), (0, 0, 0), (255, 255, 255)],
                [(255, 255, 255), (255, 255, 255), (255, 255, 255)],
            ]
        )
        terrain = TerrainMap.from_png(path, ModelConfig())

        self.assertEqual(
            terrain.validation_issues,
            ("1 restricted cells are outside the black outer boundary",),
        )
        self.assertEqual(
            terrain.to_dict()["validation_issues"],
            ["1 restricted cells are outside the black outer boundary"],
        )

    def _write_png(self, rows):
        handle = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        path = Path(handle.name)
        handle.close()
        width = len(rows[0])
        height = len(rows)
        raw = bytearray()
        for row in rows:
            raw.append(0)
            for red, green, blue in row:
                raw.extend((red, green, blue, 255))
        with path.open("wb") as png:
            png.write(b"\x89PNG\r\n\x1a\n")
            self._write_chunk(
                png,
                b"IHDR",
                struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0),
            )
            self._write_chunk(png, b"IDAT", zlib.compress(bytes(raw)))
            self._write_chunk(png, b"IEND", b"")
        return path

    def _write_chunk(self, png, chunk_type, payload):
        png.write(struct.pack(">I", len(payload)))
        png.write(chunk_type)
        png.write(payload)
        checksum = zlib.crc32(chunk_type)
        checksum = zlib.crc32(payload, checksum)
        png.write(struct.pack(">I", checksum & 0xFFFFFFFF))


if __name__ == "__main__":
    unittest.main()
