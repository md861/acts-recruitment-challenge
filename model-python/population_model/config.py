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


@dataclass(frozen=True)
class ModelConfig:
    width: int = 20
    height: int = 14
    agent_count: int = 18
    seed: int = 7
    tick_interval_seconds: float = 0.75

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
        )

