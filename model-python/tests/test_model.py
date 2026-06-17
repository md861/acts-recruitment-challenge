import unittest

from population_model.config import ModelConfig
from population_model.model import PopulationModel


class PopulationModelTests(unittest.TestCase):
    def test_snapshot_contains_agents_in_bounds(self):
        model = PopulationModel(ModelConfig(width=8, height=6, agent_count=6, seed=3))
        model.step(10)

        snapshot = model.snapshot()

        self.assertEqual(snapshot["simulation"]["agent_count"], 6)
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

        self.assertEqual(first["agents"], model.snapshot()["agents"])


if __name__ == "__main__":
    unittest.main()

