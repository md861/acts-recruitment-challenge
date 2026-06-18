## @file config.py
#  @brief Runtime configuration for the population model service.
#
#  Defines deterministic defaults and environment parsing for dimensions,
#  terrain maps, permissions, capacity, exits, and penalty settings.

import os
from dataclasses import dataclass


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _env_csv(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw = os.getenv(name)
    if raw is None:
        return default
    values = tuple(value.strip() for value in raw.split(",") if value.strip())
    return values or default


@dataclass(frozen=True)
class ModelConfig:
    width: int = 20
    height: int = 14
    agent_count: int = 18
    seed: int = 7
    tick_interval_seconds: float = 0.75
    terrain_map_path: str = "Terrain maps/Terrain1.png"
    restricted_cell_agent_ids: tuple[str, ...] = ("agent-001", "agent-002")
    restricted_cell_roles: tuple[str, ...] = ("patrol",)
    exit_cell_agent_ids: tuple[str, ...] = ("agent-001",)
    gate_max_density: int = 3
    type_1_penalty_direction: str = "east"
    type_1_penalty_multiplier: float = 0.5

    @classmethod
    def from_env(cls) -> "ModelConfig":
        return cls(
            width=_env_int("SIM_WIDTH", cls.width),
            height=_env_int("SIM_HEIGHT", cls.height),
            agent_count=_env_int("SIM_AGENT_COUNT", cls.agent_count),
            seed=_env_int("SIM_SEED", cls.seed),
            tick_interval_seconds=_env_float(
                "SIM_TICK_INTERVAL_SECONDS", cls.tick_interval_seconds
            ),
            terrain_map_path=os.getenv("SIM_TERRAIN_MAP_PATH", cls.terrain_map_path),
            restricted_cell_agent_ids=_env_csv(
                "SIM_RESTRICTED_CELL_AGENT_IDS", cls.restricted_cell_agent_ids
            ),
            restricted_cell_roles=_env_csv(
                "SIM_RESTRICTED_CELL_ROLES", cls.restricted_cell_roles
            ),
            exit_cell_agent_ids=_env_csv(
                "SIM_EXIT_CELL_AGENT_IDS", cls.exit_cell_agent_ids
            ),
            gate_max_density=_env_int("SIM_GATE_MAX_DENSITY", cls.gate_max_density),
            type_1_penalty_direction=os.getenv(
                "SIM_TYPE_1_PENALTY_DIRECTION", cls.type_1_penalty_direction
            ),
            type_1_penalty_multiplier=_env_float(
                "SIM_TYPE_1_PENALTY_MULTIPLIER", cls.type_1_penalty_multiplier
            ),
        )
