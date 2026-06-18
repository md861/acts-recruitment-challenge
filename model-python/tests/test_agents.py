import random
import unittest

from population_model.agents import AgentFactory
from population_model.config import ModelConfig
from population_model.state import Position
from population_model.terrain import CellType


class StubTerrain:
    def __init__(
        self,
        width,
        height,
        cells=None,
        inside_cells=None,
    ):
        self.width = width
        self.height = height
        self.cells = cells or {}
        self.inside_cells = inside_cells

    def cell_type_at(self, x, y):
        return self.cells.get((x, y), CellType.NORMAL)

    def is_inside_simulation_area(self, x, y):
        if self.inside_cells is None:
            return True
        return (x, y) in self.inside_cells


class AgentFactoryTests(unittest.TestCase):
    def test_agent_creation_is_deterministic_for_seed(self):
        config = ModelConfig(width=5, height=5, agent_count=6, seed=11)
        terrain = StubTerrain(width=5, height=5)

        first = AgentFactory(
            config=config,
            terrain=terrain,
            width=5,
            height=5,
            restricted_cells=set(),
        ).create_agents(random.Random(config.seed))
        second = AgentFactory(
            config=config,
            terrain=terrain,
            width=5,
            height=5,
            restricted_cells=set(),
        ).create_agents(random.Random(config.seed))

        self.assertEqual([agent.to_dict() for agent in first], [agent.to_dict() for agent in second])
        self.assertEqual(
            [agent.role for agent in first],
            ["civilian", "staff", "patrol", "civilian", "staff", "patrol"],
        )

    def test_placement_avoids_blocked_cells_and_outside_black_enclosure(self):
        terrain = StubTerrain(
            width=5,
            height=5,
            cells={
                (1, 1): CellType.BOUNDARY,
                (2, 1): CellType.DENSITY_ZERO,
                (3, 1): CellType.RESTRICTED,
            },
            inside_cells={(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2)},
        )
        config = ModelConfig(width=5, height=5, agent_count=3, seed=1)

        agents = AgentFactory(
            config=config,
            terrain=terrain,
            width=5,
            height=5,
            restricted_cells=set(),
        ).create_agents(random.Random(config.seed))
        positions = {(agent.position.x, agent.position.y) for agent in agents}

        self.assertTrue(positions <= terrain.inside_cells)
        self.assertNotIn((1, 1), positions)
        self.assertNotIn((2, 1), positions)

    def test_placement_skips_legacy_restricted_cells(self):
        terrain = StubTerrain(width=4, height=4)
        config = ModelConfig(width=4, height=4, agent_count=1, seed=1)
        factory = AgentFactory(
            config=config,
            terrain=terrain,
            width=4,
            height=4,
            restricted_cells={(0, 0)},
        )

        self.assertFalse(factory.is_available(Position(x=0, y=0), occupied=set()))


if __name__ == "__main__":
    unittest.main()
