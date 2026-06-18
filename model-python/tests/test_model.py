import unittest

from population_model.config import ModelConfig
from population_model.model import PopulationModel
from population_model.state import Agent, Heading, Position
from population_model.terrain import CellType


class PopulationModelTests(unittest.TestCase):
    def test_snapshot_contains_agents_in_bounds(self):
        model = PopulationModel(ModelConfig(width=8, height=6, agent_count=6, seed=3))
        model.step(10)

        snapshot = model.snapshot()

        self.assertEqual(snapshot["simulation"]["agent_count"], 6)
        self.assertIn("behaviour_profile", snapshot["agents"][0])
        for agent in snapshot["agents"]:
            self.assertGreaterEqual(agent["position"]["x"], 0)
            self.assertLess(agent["position"]["x"], 8)
            self.assertGreaterEqual(agent["position"]["y"], 0)
            self.assertLess(agent["position"]["y"], 6)

    def test_reset_is_repeatable(self):
        model = PopulationModel(ModelConfig(width=8, height=6, agent_count=6, seed=3))
        first = model.snapshot()
        model.step(5)
        model.reset()

        reset_snapshot = model.snapshot()
        self.assertEqual(first["agents"], reset_snapshot["agents"])
        self.assertEqual(reset_snapshot["simulation"]["tick"], 0)
        self.assertEqual(
            sum(
                cell["count"]
                for cell in reset_snapshot["simulation"]["metrics"]["cell_density"]
            ),
            reset_snapshot["simulation"]["agent_count"],
        )

    def test_snapshot_contains_terrain_map_metadata_and_metrics(self):
        model = PopulationModel(ModelConfig(width=8, height=6, agent_count=6, seed=3))
        model.step()

        snapshot = model.snapshot()

        self.assertIn("metrics", snapshot["simulation"])
        self.assertIn("map", snapshot["terrain"])
        self.assertEqual(snapshot["terrain"]["map"]["summary"]["width"], 1213)
        self.assertEqual(snapshot["terrain"]["map"]["summary"]["height"], 839)
        self.assertEqual(
            snapshot["terrain"]["map"]["summary"]["counts_by_type"]["normal"],
            854869,
        )
        metrics = snapshot["simulation"]["metrics"]
        self.assertIn("time_spent_by_agent_id", metrics)
        self.assertIn("cell_density", metrics)
        self.assertIn("congested_cells", metrics)
        self.assertEqual(
            sum(cell["count"] for cell in metrics["cell_density"]),
            snapshot["simulation"]["agent_count"],
        )

    def test_model_records_movement_strategy_block_reasons(self):
        model = PopulationModel(
            ModelConfig(width=1213, height=839, agent_count=1, seed=3)
        )
        boundary_source, _boundary_target, boundary_move = self._movement_into(
            model.terrain, CellType.BOUNDARY
        )
        model.agents = [self._agent("agent-boundary", "boundary", boundary_source)]
        model._next_movement = lambda role: boundary_move

        model.step()
        snapshot = model.snapshot()

        self.assertEqual(snapshot["agents"][0]["status"], "blocked")
        self.assertGreater(
            snapshot["simulation"]["metrics"]["blocked_boundary_attempts"],
            0,
        )

    def test_restricted_cells_are_respected_by_configured_id_and_role(self):
        config = ModelConfig(
            width=1213,
            height=839,
            agent_count=3,
            seed=3,
            restricted_cell_agent_ids=("agent-allowed",),
            restricted_cell_roles=("patrol",),
        )
        model = PopulationModel(config)
        restricted_source, restricted_target, restricted_move = self._movement_into(
            model.terrain, CellType.RESTRICTED
        )
        model.agents = [
            self._agent("agent-blocked", "civilian", restricted_source),
            self._agent("agent-allowed", "civilian", restricted_source),
            self._agent("agent-patrol", "patrol", restricted_source),
        ]
        model._next_movement = lambda role: restricted_move

        model.step()
        snapshot = model.snapshot()
        positions_by_id = {
            agent["id"]: (agent["position"]["x"], agent["position"]["y"])
            for agent in snapshot["agents"]
        }
        statuses_by_id = {
            agent["id"]: agent["status"] for agent in snapshot["agents"]
        }

        self.assertEqual(positions_by_id["agent-blocked"], restricted_source)
        self.assertEqual(statuses_by_id["agent-blocked"], "blocked")
        self.assertEqual(positions_by_id["agent-allowed"], restricted_target)
        self.assertEqual(positions_by_id["agent-patrol"], restricted_target)
        self.assertEqual(snapshot["simulation"]["metrics"]["breach_detected"], 1)
        self.assertEqual(snapshot["simulation"]["metrics"]["breach_handled"], 1)
        self.assertEqual(snapshot["simulation"]["metrics"]["unresolved_breaches"], 0)

    def test_snapshot_preserves_api_compatible_shape_with_additive_fields(self):
        model = PopulationModel(ModelConfig(width=8, height=6, agent_count=2, seed=5))

        snapshot = model.snapshot()

        self.assertEqual(set(snapshot), {"simulation", "terrain", "agents"})
        self.assertTrue(
            {
                "tick",
                "status",
                "width",
                "height",
                "agent_count",
                "seed",
                "updated_at",
            }
            <= set(snapshot["simulation"])
        )
        self.assertIn("metrics", snapshot["simulation"])
        self.assertTrue({"restricted_cells", "note"} <= set(snapshot["terrain"]))
        self.assertIn("map", snapshot["terrain"])
        self.assertTrue(
            {"id", "role", "status", "position", "heading"}
            <= set(snapshot["agents"][0])
        )

    def test_terrain_map_integration_records_metrics_over_ticks(self):
        config = ModelConfig(
            width=1213,
            height=839,
            agent_count=7,
            seed=3,
            restricted_cell_agent_ids=("agent-allowed",),
            exit_cell_agent_ids=("agent-exit",),
            gate_max_density=2,
        )
        model = PopulationModel(config)
        terrain = model.terrain
        restricted_source, restricted_target, restricted_move = self._movement_into(
            terrain, CellType.RESTRICTED
        )
        boundary_source, boundary_target, boundary_move = self._movement_into(
            terrain, CellType.BOUNDARY
        )
        gate_source, gate_target, gate_move = self._movement_into(terrain, CellType.GATE)
        exit_source, exit_target, exit_move = self._movement_into(terrain, CellType.EXIT)
        type_1_cell = self._first_cell(terrain, CellType.TYPE_1_PENALTY)
        type_2_cell = self._first_cell(terrain, CellType.TYPE_2_PENALTY)
        normal_cell = self._first_cell(terrain, CellType.NORMAL)

        model.agents = [
            self._agent("agent-blocked", "restricted", restricted_source),
            self._agent("agent-boundary", "boundary", boundary_source),
            self._agent("agent-gate-a", "gate_a", gate_target),
            self._agent("agent-gate-b", "gate_b", gate_target),
            self._agent("agent-gate-c", "gate_c", gate_source),
            self._agent("agent-exit", "exit", exit_source),
            self._agent("agent-type-1", "type_1", type_1_cell),
            self._agent("agent-type-2", "type_2", type_2_cell),
            self._agent("agent-normal", "normal", normal_cell),
        ]
        moves_by_role = {
            "restricted": restricted_move,
            "boundary": boundary_move,
            "gate_a": (0, 0),
            "gate_b": (0, 0),
            "gate_c": gate_move,
            "exit": exit_move,
            "type_1": (0, 0),
            "type_2": (0, 0),
            "normal": (0, 0),
        }
        model._next_movement = lambda role: moves_by_role[role]

        model.step(100)
        metrics = model.snapshot()["simulation"]["metrics"]

        self.assertGreater(metrics["breach_detected"], 0)
        self.assertEqual(metrics["breach_detected"], metrics["breach_handled"])
        self.assertGreater(metrics["blocked_boundary_attempts"], 0)
        self.assertGreater(metrics["gate_congestion_events"], 0)
        self.assertGreater(metrics["congestion_count"], 0)
        self.assertGreater(len(metrics["congested_cells"]), 0)
        self.assertGreater(metrics["exit_events"], 0)
        self.assertGreater(metrics["penalty_cell_traversals"], 0)
        self.assertGreater(
            metrics["time_spent_by_agent_id"]["agent-blocked"]["normal"], 0
        )
        self.assertGreater(
            metrics["time_spent_by_agent_id"]["agent-type-1"]["type_1_penalty"], 0
        )
        self.assertGreater(
            metrics["time_spent_by_agent_id"]["agent-type-2"]["type_2_penalty"], 0
        )
        self.assertEqual(terrain.cell_type_at(*restricted_target), CellType.RESTRICTED)
        self.assertEqual(terrain.cell_type_at(*boundary_target), CellType.BOUNDARY)
        self.assertEqual(terrain.cell_type_at(*exit_target), CellType.EXIT)

    def _agent(self, agent_id, role, position):
        return Agent(
            id=agent_id,
            role=role,
            status="waiting",
            position=Position(x=position[0], y=position[1]),
            heading=Heading(dx=0, dy=0),
        )

    def _first_cell(self, terrain, cell_type):
        for index, candidate in enumerate(terrain.cell_types):
            if candidate == cell_type:
                return (index % terrain.width, index // terrain.width)
        self.fail(f"No cell found for {cell_type.value}")

    def _movement_into(self, terrain, target_type):
        for index, candidate in enumerate(terrain.cell_types):
            if candidate != target_type:
                continue
            target = (index % terrain.width, index // terrain.width)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                source = (target[0] - dx, target[1] - dy)
                if source[0] < 0 or source[1] < 0:
                    continue
                if source[0] >= terrain.width or source[1] >= terrain.height:
                    continue
                if terrain.cell_type_at(*source) == CellType.NORMAL:
                    return source, target, (dx, dy)
        self.fail(f"No normal source found adjacent to {target_type.value}")


if __name__ == "__main__":
    unittest.main()
