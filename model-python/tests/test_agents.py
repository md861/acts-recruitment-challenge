import random
import unittest

from population_model.agents import AgentFactory
from population_model.behaviour import BehaviourProfile, BehaviourProfileSet
from population_model.config import ModelConfig
from population_model.random_walk import RandomWalkPolicy
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

        self.assertEqual(
            [agent.to_dict() for agent in first],
            [agent.to_dict() for agent in second],
        )
        self.assertEqual(
            [agent.role for agent in first],
            ["civilian", "staff", "patrol", "civilian", "staff", "patrol"],
        )
        self.assertEqual(
            [agent.behaviour_profile for agent in first],
            ["civilian", "staff", "patrol", "civilian", "staff", "patrol"],
        )

    def test_agent_creation_uses_configured_behaviour_profile_lookup(self):
        config = ModelConfig(width=3, height=3, agent_count=1, seed=1)
        terrain = StubTerrain(width=3, height=3)
        behaviour_profiles = BehaviourProfileSet(
            profiles={
                "visitor": BehaviourProfile(
                    role="guest-profile",
                    random_walk=RandomWalkPolicy.uniform(((0, 0),)),
                )
            },
            default_role="visitor",
        )

        agents = AgentFactory(
            config=config,
            terrain=terrain,
            width=3,
            height=3,
            restricted_cells=set(),
            roles=("visitor",),
            behaviour_profiles=behaviour_profiles,
        ).create_agents(random.Random(config.seed))

        self.assertEqual(agents[0].role, "visitor")
        self.assertEqual(agents[0].behaviour_profile, "guest-profile")

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

    def test_placement_can_seed_agents_across_allowed_non_black_cell_types(self):
        cells = {
            (0, 0): CellType.NORMAL,
            (1, 0): CellType.RESTRICTED,
            (2, 0): CellType.GATE,
            (0, 1): CellType.EXIT,
            (1, 1): CellType.TYPE_1_PENALTY,
            (2, 1): CellType.TYPE_2_PENALTY,
            (0, 2): CellType.BOUNDARY,
            (1, 2): CellType.DENSITY_ZERO,
        }
        terrain = StubTerrain(
            width=3,
            height=3,
            cells=cells,
            inside_cells=set(cells),
        )
        config = ModelConfig(width=3, height=3, agent_count=6, seed=2)

        agents = AgentFactory(
            config=config,
            terrain=terrain,
            width=3,
            height=3,
            restricted_cells=set(),
        ).create_agents(random.Random(config.seed))
        placed_cell_types = {
            terrain.cell_type_at(agent.position.x, agent.position.y)
            for agent in agents
        }

        self.assertEqual(
            placed_cell_types,
            {
                CellType.NORMAL,
                CellType.RESTRICTED,
                CellType.GATE,
                CellType.EXIT,
                CellType.TYPE_1_PENALTY,
                CellType.TYPE_2_PENALTY,
            },
        )


if __name__ == "__main__":
    unittest.main()
