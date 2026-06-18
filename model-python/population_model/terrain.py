## @file terrain.py
#  @brief PNG-backed terrain map parsing and cell rule queries.
#
#  Converts terrain map pixels into symbolic cell types, validates map
#  enclosure semantics, and exposes traversal, capacity, breach, exit, and
#  penalty queries for simulation modules.

import struct
import zlib
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from population_model.config import ModelConfig


class CellType(str, Enum):
    NORMAL = "normal"
    BOUNDARY = "boundary"
    DENSITY_ZERO = "density_zero"
    RESTRICTED = "restricted"
    GATE = "gate"
    EXIT = "exit"
    TYPE_1_PENALTY = "type_1_penalty"
    TYPE_2_PENALTY = "type_2_penalty"


PALETTE: dict[tuple[int, int, int], CellType] = {
    (255, 255, 255): CellType.NORMAL,
    (0, 0, 0): CellType.BOUNDARY,
    (136, 0, 21): CellType.DENSITY_ZERO,
    (185, 122, 87): CellType.DENSITY_ZERO,
    (237, 28, 36): CellType.RESTRICTED,
    (255, 127, 39): CellType.GATE,
    (34, 177, 76): CellType.EXIT,
    (63, 72, 204): CellType.TYPE_1_PENALTY,
    (255, 174, 201): CellType.TYPE_2_PENALTY,
}

LEGEND = {cell_type.value: color for color, cell_type in PALETTE.items()}


@dataclass(frozen=True)
class TerrainPenalty:
    ## @brief Movement penalty metadata attached to penalty cells.
    kind: str
    direction: str | None = None
    multiplier: float | None = None

    def to_dict(self) -> dict:
        payload: dict[str, str | float] = {"kind": self.kind}
        if self.direction is not None:
            payload["direction"] = self.direction
        if self.multiplier is not None:
            payload["multiplier"] = self.multiplier
        return payload


@dataclass(frozen=True)
class TerrainCell:
    ## @brief Symbolic terrain cell definition and configured rule metadata.
    x: int
    y: int
    cell_type: CellType
    allowed_agent_ids: tuple[str, ...] = ()
    allowed_roles: tuple[str, ...] = ()
    exit_agent_ids: tuple[str, ...] = ()
    max_density: int | None = None
    penalty: TerrainPenalty | None = None

    def to_dict(self) -> dict:
        payload: dict[str, object] = {
            "x": self.x,
            "y": self.y,
            "type": self.cell_type.value,
        }
        if self.allowed_agent_ids:
            payload["allowed_agent_ids"] = list(self.allowed_agent_ids)
        if self.allowed_roles:
            payload["allowed_roles"] = list(self.allowed_roles)
        if self.exit_agent_ids:
            payload["exit_agent_ids"] = list(self.exit_agent_ids)
        if self.max_density is not None:
            payload["max_density"] = self.max_density
        if self.penalty is not None:
            payload["penalty"] = self.penalty.to_dict()
        return payload


@dataclass(frozen=True)
class TerrainTraversal:
    ## @brief Terrain-level classification of a traversal attempt.
    #
    #  Centralizes role/id permissions, boundary blocking, gate congestion, and
    #  restricted-cell breach classification so movement and metrics can consume
    #  the same reason metadata.
    allowed: bool
    reason: str
    cell: TerrainCell
    breach_detected: bool = False
    breach_handled: bool = True


@dataclass(frozen=True)
class TerrainSummary:
    ## @brief Aggregate terrain map dimensions, cell counts, and validation issues.
    width: int
    height: int
    counts_by_type: dict[CellType, int]
    validation_issues: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "counts_by_type": {
                cell_type.value: self.counts_by_type.get(cell_type, 0)
                for cell_type in CellType
            },
            "validation_issues": list(self.validation_issues),
        }


@dataclass(frozen=True)
class TerrainMap:
    ## @brief Parsed terrain map and terrain-rule query API.
    width: int
    height: int
    cell_types: tuple[CellType, ...]
    config: ModelConfig
    source_path: Path
    enclosed_cells: frozenset[tuple[int, int]]
    validation_issues: tuple[str, ...] = ()

    @classmethod
    def from_png(cls, path: str | Path, config: ModelConfig) -> "TerrainMap":
        source_path = _resolve_terrain_path(Path(path))
        width, height, pixels = _read_png_rgb(source_path)
        cell_types: list[CellType] = []
        for rgb in pixels:
            try:
                cell_types.append(PALETTE[rgb])
            except KeyError as exc:
                raise ValueError(
                    f"Unsupported terrain color {rgb} in {source_path}"
                ) from exc
        return cls(
            width=width,
            height=height,
            cell_types=tuple(cell_types),
            config=config,
            source_path=source_path,
            enclosed_cells=_find_enclosed_cells(width, height, tuple(cell_types)),
            validation_issues=_validate_cell_definitions(
                width, height, tuple(cell_types)
            ),
        )

    def cell_type_at(self, x: int, y: int) -> CellType:
        self._check_bounds(x, y)
        return self.cell_types[self._index(x, y)]

    def cell_at(self, x: int, y: int) -> TerrainCell:
        cell_type = self.cell_type_at(x, y)
        return TerrainCell(
            x=x,
            y=y,
            cell_type=cell_type,
            allowed_agent_ids=self._allowed_agent_ids(cell_type),
            allowed_roles=self._allowed_roles(cell_type),
            exit_agent_ids=self._exit_agent_ids(cell_type),
            max_density=self._max_density(cell_type),
            penalty=self._penalty(cell_type),
        )

    def is_traversable(
        self,
        x: int,
        y: int,
        agent_id: str,
        current_density: int = 0,
        agent_role: str | None = None,
    ) -> bool:
        return self.classify_traversal(
            x,
            y,
            agent_id=agent_id,
            current_density=current_density,
            agent_role=agent_role,
        ).allowed

    def classify_traversal(
        self,
        x: int,
        y: int,
        agent_id: str,
        current_density: int = 0,
        agent_role: str | None = None,
    ) -> TerrainTraversal:
        ## @brief Classify one attempted terrain entry.
        #
        #  Restricted cells can permit either configured agent ids or configured
        #  roles. Unauthorized restricted-cell attempts are classified as handled
        #  breaches rather than generic blocked movement.
        cell = self.cell_at(x, y)
        if not self.is_inside_simulation_area(x, y):
            return TerrainTraversal(False, "outside_enclosure", cell)
        if cell.cell_type in (CellType.BOUNDARY, CellType.DENSITY_ZERO):
            return TerrainTraversal(False, "boundary", cell)
        if cell.cell_type == CellType.RESTRICTED:
            if agent_id in cell.allowed_agent_ids or (
                agent_role is not None and agent_role in cell.allowed_roles
            ):
                return TerrainTraversal(True, "allowed", cell)
            return TerrainTraversal(
                False,
                "restricted",
                cell,
                breach_detected=True,
                breach_handled=True,
            )
        if cell.cell_type == CellType.GATE and cell.max_density is not None:
            if current_density >= cell.max_density:
                return TerrainTraversal(False, "gate_congestion", cell)
        return TerrainTraversal(True, "allowed", cell)

    def is_exit_cell(self, x: int, y: int, agent_id: str) -> bool:
        cell = self.cell_at(x, y)
        return cell.cell_type == CellType.EXIT and agent_id in cell.exit_agent_ids

    def penalty_at(self, x: int, y: int) -> TerrainPenalty | None:
        return self.cell_at(x, y).penalty

    def is_inside_simulation_area(self, x: int, y: int) -> bool:
        self._check_bounds(x, y)
        return (x, y) in self.enclosed_cells

    def summary(self) -> TerrainSummary:
        counts = Counter(self.cell_types)
        return TerrainSummary(
            width=self.width,
            height=self.height,
            counts_by_type={cell_type: counts.get(cell_type, 0) for cell_type in CellType},
            validation_issues=self.validation_issues,
        )

    def to_dict(self) -> dict:
        return {
            "source": str(self.source_path),
            "asset_path": f"/terrain/{self.source_path.name}",
            "validation_issues": list(self.validation_issues),
            "legend": {
                cell_type_name: {"r": rgb[0], "g": rgb[1], "b": rgb[2]}
                for cell_type_name, rgb in LEGEND.items()
            },
            "summary": self.summary().to_dict(),
        }

    def _index(self, x: int, y: int) -> int:
        return y * self.width + x

    def _check_bounds(self, x: int, y: int) -> None:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError(f"Terrain position out of bounds: ({x}, {y})")

    def _allowed_agent_ids(self, cell_type: CellType) -> tuple[str, ...]:
        if cell_type == CellType.RESTRICTED:
            return self.config.restricted_cell_agent_ids
        return ()

    def _allowed_roles(self, cell_type: CellType) -> tuple[str, ...]:
        if cell_type == CellType.RESTRICTED:
            return self.config.restricted_cell_roles
        return ()

    def _exit_agent_ids(self, cell_type: CellType) -> tuple[str, ...]:
        if cell_type == CellType.EXIT:
            return self.config.exit_cell_agent_ids
        return ()

    def _max_density(self, cell_type: CellType) -> int | None:
        if cell_type == CellType.GATE:
            return self.config.gate_max_density
        return None

    def _penalty(self, cell_type: CellType) -> TerrainPenalty | None:
        if cell_type == CellType.TYPE_1_PENALTY:
            return TerrainPenalty(
                kind="type_1",
                direction=self.config.type_1_penalty_direction,
                multiplier=self.config.type_1_penalty_multiplier,
            )
        if cell_type == CellType.TYPE_2_PENALTY:
            return TerrainPenalty(kind="type_2", multiplier=0.5)
        return None


def load_terrain_map(config: ModelConfig) -> TerrainMap:
    return TerrainMap.from_png(config.terrain_map_path, config)


def _resolve_terrain_path(path: Path) -> Path:
    if path.is_absolute() or path.exists():
        return path
    package_dir = Path(__file__).resolve().parent
    for root in (*package_dir.parents, Path.cwd(), *Path.cwd().parents):
        candidate = root / path
        if candidate.exists():
            return candidate
    return path


def _find_enclosed_cells(
    width: int, height: int, cell_types: tuple[CellType, ...]
) -> frozenset[tuple[int, int]]:
    outside = _flood_fill_outside_boundary(width, height, cell_types)
    enclosed = set()
    for y in range(height):
        for x in range(width):
            key = (x, y)
            cell_type = cell_types[y * width + x]
            if cell_type == CellType.BOUNDARY:
                enclosed.add(key)
            elif key not in outside:
                enclosed.add(key)
    return frozenset(enclosed)


def _validate_cell_definitions(
    width: int, height: int, cell_types: tuple[CellType, ...]
) -> tuple[str, ...]:
    outside = _flood_fill_outside_boundary(width, height, cell_types)
    outside_definitions = Counter()
    for x, y in outside:
        cell_type = cell_types[y * width + x]
        if cell_type not in (CellType.NORMAL, CellType.BOUNDARY):
            outside_definitions[cell_type] += 1

    issues = []
    for cell_type, count in sorted(
        outside_definitions.items(), key=lambda item: item[0].value
    ):
        issues.append(
            f"{count} {cell_type.value} cells are outside the black outer boundary"
        )
    return tuple(issues)


def _flood_fill_outside_boundary(
    width: int, height: int, cell_types: tuple[CellType, ...]
) -> set[tuple[int, int]]:
    outside: set[tuple[int, int]] = set()
    queue: list[tuple[int, int]] = []

    def add_if_open(x: int, y: int) -> None:
        if x < 0 or x >= width or y < 0 or y >= height:
            return
        if (x, y) in outside:
            return
        if cell_types[y * width + x] == CellType.BOUNDARY:
            return
        outside.add((x, y))
        queue.append((x, y))

    for x in range(width):
        add_if_open(x, 0)
        add_if_open(x, height - 1)
    for y in range(height):
        add_if_open(0, y)
        add_if_open(width - 1, y)

    while queue:
        x, y = queue.pop()
        add_if_open(x + 1, y)
        add_if_open(x - 1, y)
        add_if_open(x, y + 1)
        add_if_open(x, y - 1)

    return outside


def _read_png_rgb(path: Path) -> tuple[int, int, list[tuple[int, int, int]]]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG file")

    width = height = bit_depth = color_type = interlace = None
    idat_chunks: list[bytes] = []
    pos = 8
    while pos < len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        chunk_type = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        pos += length + 12

        if chunk_type == b"IHDR":
            (
                width,
                height,
                bit_depth,
                color_type,
                _compression,
                _filter,
                interlace,
            ) = struct.unpack(">IIBBBBB", chunk)
        elif chunk_type == b"IDAT":
            idat_chunks.append(chunk)
        elif chunk_type == b"IEND":
            break

    if width is None or height is None or bit_depth is None or color_type is None:
        raise ValueError(f"{path} is missing a valid PNG header")
    if bit_depth != 8 or color_type not in (2, 6) or interlace != 0:
        raise ValueError(
            f"{path} must be an 8-bit non-interlaced RGB or RGBA PNG"
        )

    channels = 4 if color_type == 6 else 3
    row_size = width * channels
    raw = zlib.decompress(b"".join(idat_chunks))
    rows = _unfilter_png_rows(raw, width=width, height=height, channels=channels)
    pixels: list[tuple[int, int, int]] = []
    for row in rows:
        for index in range(0, len(row), channels):
            pixels.append((row[index], row[index + 1], row[index + 2]))
    if len(pixels) != width * height:
        raise ValueError(f"{path} decoded to an unexpected number of pixels")
    return width, height, pixels


def _unfilter_png_rows(
    raw: bytes, width: int, height: int, channels: int
) -> list[bytearray]:
    row_size = width * channels
    previous = bytearray(row_size)
    rows: list[bytearray] = []
    offset = 0

    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        scanline = bytearray(raw[offset : offset + row_size])
        offset += row_size
        row = bytearray(row_size)

        for index, value in enumerate(scanline):
            left = row[index - channels] if index >= channels else 0
            up = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            predictor = _png_filter_predictor(filter_type, left, up, upper_left)
            row[index] = (value + predictor) & 0xFF

        rows.append(row)
        previous = row

    return rows


def _png_filter_predictor(
    filter_type: int, left: int, up: int, upper_left: int
) -> int:
    if filter_type == 0:
        return 0
    if filter_type == 1:
        return left
    if filter_type == 2:
        return up
    if filter_type == 3:
        return (left + up) // 2
    if filter_type == 4:
        estimate = left + up - upper_left
        left_distance = abs(estimate - left)
        up_distance = abs(estimate - up)
        upper_left_distance = abs(estimate - upper_left)
        if left_distance <= up_distance and left_distance <= upper_left_distance:
            return left
        if up_distance <= upper_left_distance:
            return up
        return upper_left
    raise ValueError(f"Unsupported PNG filter type: {filter_type}")
