import random
from datetime import datetime, timezone

from population_model.config import ModelConfig
from population_model.state import Agent, Heading, Position


class PopulationModel:
    """A deliberately simple population model.

    The model is intentionally naive: agents perform a random walk on a bounded
    lattice and do not yet use intent, routes, congestion, or terrain costs.
    """

    def __init__(self, config: ModelConfig):
        self.config = config
        self._rng = random.Random(config.seed)
        self.tick = 0
        self.agents = self._create_agents()

    def reset(self) -> None:
        self._rng = random.Random(self.config.seed)
        self.tick = 0
        self.agents = self._create_agents()

    def step(self, ticks: int = 1) -> None:
        for _ in range(max(1, ticks)):
            self.tick += 1
            for agent in self.agents:
                dx, dy = self._next_movement(agent.role)
                agent.heading = Heading(dx=dx, dy=dy)
                agent.position.x = self._clamp(agent.position.x + dx, 0, self.config.width - 1)
                agent.position.y = self._clamp(agent.position.y + dy, 0, self.config.height - 1)
                agent.status = "waiting" if dx == 0 and dy == 0 else "moving"

    def snapshot(self) -> dict:
        return {
            "simulation": {
                "tick": self.tick,
                "status": "running",
                "width": self.config.width,
                "height": self.config.height,
                "agent_count": len(self.agents),
                "seed": self.config.seed,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
            "terrain": {
                "restricted_cells": [
                    {"x": x, "y": y} for x, y in self._restricted_cells()
                ],
                "note": "The baseline model shows restricted cells but does not route agents around them.",
            },
            "agents": [agent.to_dict() for agent in self.agents],
        }

    def _create_agents(self) -> list[Agent]:
        roles = ["civilian", "staff", "patrol"]
        agents: list[Agent] = []
        occupied: set[tuple[int, int]] = set()
        restricted = set(self._restricted_cells())

        for index in range(self.config.agent_count):
            role = roles[index % len(roles)]
            position = self._random_free_position(occupied, restricted)
            occupied.add((position.x, position.y))
            agents.append(
                Agent(
                    id=f"agent-{index + 1:03d}",
                    role=role,
                    status="waiting",
                    position=position,
                    heading=Heading(dx=0, dy=0),
                )
            )

        return agents

    def _random_free_position(
        self, occupied: set[tuple[int, int]], restricted: set[tuple[int, int]]
    ) -> Position:
        for _ in range(200):
            position = Position(
                x=self._rng.randrange(self.config.width),
                y=self._rng.randrange(self.config.height),
            )
            key = (position.x, position.y)
            if key not in occupied and key not in restricted:
                return position
        return Position(x=0, y=0)

    def _next_movement(self, role: str) -> tuple[int, int]:
        if role == "patrol":
            choices = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif role == "staff":
            choices = [(0, 0), (1, 0), (0, 1), (-1, 0)]
        else:
            choices = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
        return self._rng.choice(choices)

    def _restricted_cells(self) -> list[tuple[int, int]]:
        mid_x = self.config.width // 2
        mid_y = self.config.height // 2
        return [
            (mid_x - 1, mid_y - 1),
            (mid_x, mid_y - 1),
            (mid_x - 1, mid_y),
            (mid_x, mid_y),
        ]

    @staticmethod
    def _clamp(value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, value))

