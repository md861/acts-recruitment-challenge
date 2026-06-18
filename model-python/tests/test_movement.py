import unittest

from population_model.movement import MovementStrategy
from population_model.state import Agent, Heading, Position
from population_model.terrain import CellType, TerrainCell, TerrainPenalty, TerrainTraversal


class StubTerrain:
    def __init__(
        self,
        width=4,
        height=4,
        cells=None,
        penalties=None,
        inside_cells=None,
        gate_max=1,
    ):
        self.width = width
        self.height = height
        self.cells = cells or {}
        self.penalties = penalties or {}
        self.inside_cells = inside_cells
        self.gate_max = gate_max

    def cell_type_at(self, x, y):
        return self.cells.get((x, y), CellType.NORMAL)

    def is_inside_simulation_area(self, x, y):
        if self.inside_cells is None:
            return True
        return (x, y) in self.inside_cells

    def is_traversable(self, x, y, agent_id, current_density=0, agent_role=None):
        cell_type = self.cell_type_at(x, y)
        if cell_type == CellType.RESTRICTED:
            return agent_id == "agent-allowed" or agent_role == "patrol"
        if cell_type == CellType.GATE:
            return current_density < self.gate_max
        return cell_type not in (CellType.BOUNDARY, CellType.DENSITY_ZERO)

    def penalty_at(self, x, y):
        return self.penalties.get((x, y))

    def classify_traversal(
        self, x, y, agent_id, current_density=0, agent_role=None
    ):
        cell_type = self.cell_type_at(x, y)
        cell = TerrainCell(x=x, y=y, cell_type=cell_type)
        if cell_type in (CellType.BOUNDARY, CellType.DENSITY_ZERO):
            return TerrainTraversal(False, "boundary", cell)
        if cell_type == CellType.RESTRICTED and not self.is_traversable(
            x, y, agent_id, current_density, agent_role
        ):
            return TerrainTraversal(
                False,
                "restricted",
                cell,
                breach_detected=True,
            )
        if cell_type == CellType.GATE and not self.is_traversable(
            x, y, agent_id, current_density, agent_role
        ):
            return TerrainTraversal(False, "gate_congestion", cell)
        return TerrainTraversal(True, "allowed", cell)


class MovementStrategyTests(unittest.TestCase):
    def test_allows_normal_move_with_reason_metadata(self):
        strategy = MovementStrategy(terrain=StubTerrain(), width=4, height=4)

        decision = strategy.decide(self._agent(position=(1, 1)), (1, 0))

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "allowed")
        self.assertEqual((decision.target_x, decision.target_y), (2, 1))
        self.assertEqual(decision.cell_type, CellType.NORMAL)

    def test_blocks_boundary_and_density_zero_cells(self):
        strategy = MovementStrategy(
            terrain=StubTerrain(
                cells={
                    (2, 1): CellType.BOUNDARY,
                    (1, 2): CellType.DENSITY_ZERO,
                }
            ),
            width=4,
            height=4,
        )

        boundary = strategy.decide(self._agent(position=(1, 1)), (1, 0))
        density_zero = strategy.decide(self._agent(position=(1, 1)), (0, 1))

        self.assertFalse(boundary.allowed)
        self.assertEqual(boundary.reason, "boundary")
        self.assertFalse(density_zero.allowed)
        self.assertEqual(density_zero.reason, "boundary")

    def test_blocks_moves_outside_terrain_enclosure(self):
        strategy = MovementStrategy(
            terrain=StubTerrain(width=4, height=4, inside_cells={(1, 1)}),
            width=4,
            height=4,
        )

        decision = strategy.decide(self._agent(position=(1, 1)), (1, 0))

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "outside_enclosure")

    def test_restricted_cells_use_agent_permissions(self):
        strategy = MovementStrategy(
            terrain=StubTerrain(cells={(2, 1): CellType.RESTRICTED}),
            width=4,
            height=4,
        )

        blocked = strategy.decide(self._agent(agent_id="agent-blocked"), (1, 0))
        allowed = strategy.decide(self._agent(agent_id="agent-allowed"), (1, 0))

        self.assertFalse(blocked.allowed)
        self.assertEqual(blocked.reason, "restricted")
        self.assertTrue(allowed.allowed)

    def test_gate_cells_apply_current_density_limit(self):
        strategy = MovementStrategy(
            terrain=StubTerrain(cells={(2, 1): CellType.GATE}, gate_max=2),
            width=4,
            height=4,
        )

        allowed = strategy.decide(
            self._agent(position=(1, 1)), (1, 0), current_density=1
        )
        blocked = strategy.decide(
            self._agent(position=(1, 1)), (1, 0), current_density=2
        )

        self.assertTrue(allowed.allowed)
        self.assertFalse(blocked.allowed)
        self.assertEqual(blocked.reason, "gate_congestion")

    def test_non_terrain_dimensions_allow_cells_outside_map_as_normal(self):
        strategy = MovementStrategy(
            terrain=StubTerrain(width=2, height=2),
            width=4,
            height=4,
        )

        decision = strategy.decide(self._agent(position=(2, 1)), (1, 0))

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.cell_type, CellType.NORMAL)

    def test_type_1_penalty_adds_directional_preference_cost(self):
        strategy = MovementStrategy(
            terrain=StubTerrain(
                cells={(2, 1): CellType.TYPE_1_PENALTY},
                penalties={
                    (2, 1): TerrainPenalty(
                        kind="type_1",
                        direction="east",
                        multiplier=0.5,
                    )
                },
            ),
            width=4,
            height=4,
        )

        decision = strategy.decide(self._agent(position=(1, 1)), (1, 0))

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.cell_type, CellType.TYPE_1_PENALTY)
        self.assertEqual(decision.preference_cost, 2.0)
        self.assertEqual(decision.penalty.kind, "type_1")

    def test_type_2_penalty_adds_all_direction_preference_cost(self):
        strategy = MovementStrategy(
            terrain=StubTerrain(
                cells={(1, 2): CellType.TYPE_2_PENALTY},
                penalties={(1, 2): TerrainPenalty(kind="type_2", multiplier=0.5)},
            ),
            width=4,
            height=4,
        )

        decision = strategy.decide(self._agent(position=(1, 1)), (0, 1))

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.cell_type, CellType.TYPE_2_PENALTY)
        self.assertEqual(decision.preference_cost, 2.0)
        self.assertEqual(decision.penalty.kind, "type_2")

    def _agent(self, agent_id="agent-001", position=(1, 1)):
        return Agent(
            id=agent_id,
            role="civilian",
            status="waiting",
            position=Position(x=position[0], y=position[1]),
            heading=Heading(dx=0, dy=0),
        )


if __name__ == "__main__":
    unittest.main()
