## @file test_config.py
#  @brief Unit tests for population model runtime configuration parsing.
#
#  Verifies deterministic defaults, numeric environment parsing, comma-separated
#  permission lists, and invalid environment fallbacks independently from model
#  orchestration.

import os
import unittest
from unittest.mock import patch

from population_model.config import ModelConfig


class ModelConfigTests(unittest.TestCase):
    def test_from_env_uses_deterministic_defaults_without_environment(self):
        with patch.dict(os.environ, {}, clear=True):
            config = ModelConfig.from_env()

        self.assertEqual(config.width, ModelConfig.width)
        self.assertEqual(config.height, ModelConfig.height)
        self.assertEqual(config.agent_count, ModelConfig.agent_count)
        self.assertEqual(config.seed, ModelConfig.seed)
        self.assertEqual(
            config.tick_interval_seconds,
            ModelConfig.tick_interval_seconds,
        )
        self.assertEqual(config.terrain_map_path, ModelConfig.terrain_map_path)

    def test_from_env_parses_numeric_and_terrain_values(self):
        with patch.dict(
            os.environ,
            {
                "SIM_WIDTH": "31",
                "SIM_HEIGHT": "17",
                "SIM_AGENT_COUNT": "9",
                "SIM_SEED": "42",
                "SIM_TICK_INTERVAL_SECONDS": "0.25",
                "SIM_TERRAIN_MAP_PATH": "Terrain maps/Custom.png",
                "SIM_GATE_MAX_DENSITY": "4",
                "SIM_TYPE_1_PENALTY_DIRECTION": "north",
                "SIM_TYPE_1_PENALTY_MULTIPLIER": "0.3",
            },
            clear=True,
        ):
            config = ModelConfig.from_env()

        self.assertEqual(config.width, 31)
        self.assertEqual(config.height, 17)
        self.assertEqual(config.agent_count, 9)
        self.assertEqual(config.seed, 42)
        self.assertEqual(config.tick_interval_seconds, 0.25)
        self.assertEqual(config.terrain_map_path, "Terrain maps/Custom.png")
        self.assertEqual(config.gate_max_density, 4)
        self.assertEqual(config.type_1_penalty_direction, "north")
        self.assertEqual(config.type_1_penalty_multiplier, 0.3)

    def test_from_env_parses_permission_lists_and_falls_back_on_empty_lists(self):
        with patch.dict(
            os.environ,
            {
                "SIM_RESTRICTED_CELL_AGENT_IDS": "agent-a, agent-b,,",
                "SIM_RESTRICTED_CELL_ROLES": "patrol, staff",
                "SIM_EXIT_CELL_AGENT_IDS": "agent-exit",
            },
            clear=True,
        ):
            config = ModelConfig.from_env()

        self.assertEqual(config.restricted_cell_agent_ids, ("agent-a", "agent-b"))
        self.assertEqual(config.restricted_cell_roles, ("patrol", "staff"))
        self.assertEqual(config.exit_cell_agent_ids, ("agent-exit",))

        with patch.dict(
            os.environ,
            {"SIM_RESTRICTED_CELL_AGENT_IDS": " , , "},
            clear=True,
        ):
            config = ModelConfig.from_env()

        self.assertEqual(
            config.restricted_cell_agent_ids,
            ModelConfig.restricted_cell_agent_ids,
        )

    def test_from_env_falls_back_on_invalid_numbers(self):
        with patch.dict(
            os.environ,
            {
                "SIM_WIDTH": "wide",
                "SIM_TICK_INTERVAL_SECONDS": "soon",
                "SIM_TYPE_1_PENALTY_MULTIPLIER": "heavy",
            },
            clear=True,
        ):
            config = ModelConfig.from_env()

        self.assertEqual(config.width, ModelConfig.width)
        self.assertEqual(
            config.tick_interval_seconds,
            ModelConfig.tick_interval_seconds,
        )
        self.assertEqual(
            config.type_1_penalty_multiplier,
            ModelConfig.type_1_penalty_multiplier,
        )


if __name__ == "__main__":
    unittest.main()
