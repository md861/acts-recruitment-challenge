import random
from collections import Counter
from datetime import datetime, timezone

from population_model.agents import AgentFactory
from population_model.behaviour import (
    DEFAULT_BEHAVIOUR_PROFILES,
    BehaviourProfileSet,
)
from population_model.config import ModelConfig
from population_model.metrics import TerrainMetrics
from population_model.state import Agent, Heading, Position
from population_model.terrain import CellType, load_terrain_map


class PopulationModel:
    """A deliberately simple population model.

    The model is intentionally naive: agents perform a random walk on a bounded
    lattice and do not yet use intent, routes, congestion, or terrain costs.
    """

    def __init__(self, config: ModelConfig):
        self.config = config
        self._rng = random.Random(config.seed)
        self.terrain = load_terrain_map(config)
        self.width = self.terrain.width if self._uses_default_dimensions() else config.width
        self.height = self.terrain.height if self._uses_default_dimensions() else config.height
        self.metrics = TerrainMetrics()
        self.behaviour_profiles: BehaviourProfileSet = DEFAULT_BEHAVIOUR_PROFILES
        self.tick = 0
        self.agents = self._create_agents()

    def reset(self) -> None:
        self._rng = random.Random(self.config.seed)
        self.metrics = TerrainMetrics()
        self.tick = 0
        self.agents = self._create_agents()

    def step(self, ticks: int = 1) -> None:
        for _ in range(max(1, ticks)):
            self.tick += 1
            density = self._agent_density()
            for agent in self.agents:
                dx, dy = self._next_movement(agent.role)
                target_x = self._clamp(agent.position.x + dx, 0, self.width - 1)
                target_y = self._clamp(agent.position.y + dy, 0, self.height - 1)
                current_key = (agent.position.x, agent.position.y)
                target_key = (target_x, target_y)
                target_density = density.get(target_key, 0)
                if target_key == current_key:
                    target_density = max(0, target_density - 1)

                agent.heading = Heading(dx=dx, dy=dy)
                if self._can_enter(agent, target_x, target_y, target_density):
                    agent.position.x = target_x
                    agent.position.y = target_y
                    cell_type = self._terrain_cell_type(target_x, target_y)
                    if cell_type in (CellType.TYPE_1_PENALTY, CellType.TYPE_2_PENALTY):
                        self.metrics.record_penalty_traversal()
                    if self.terrain.is_exit_cell(target_x, target_y, agent.id):
                        self.metrics.record_exit()
                    agent.status = "waiting" if dx == 0 and dy == 0 else "moving"
                else:
                    agent.status = "blocked"

                self.metrics.record_cell_time(
                    agent.id, self._terrain_cell_type(agent.position.x, agent.position.y)
                )
                density[current_key] = max(0, density.get(current_key, 0) - 1)
                density[(agent.position.x, agent.position.y)] = (
                    density.get((agent.position.x, agent.position.y), 0) + 1
                )

    def snapshot(self) -> dict:
        return {
            "simulation": {
                "tick": self.tick,
                "status": "running",
                "width": self.width,
                "height": self.height,
                "agent_count": len(self.agents),
                "seed": self.config.seed,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "metrics": self.metrics.to_dict(),
            },
            "terrain": {
                "restricted_cells": [
                    {"x": x, "y": y} for x, y in self._restricted_cells()
                ],
                "note": "The baseline model shows restricted cells but does not route agents around them.",
                "map": self.terrain.to_dict(),
            },
            "agents": [agent.to_dict() for agent in self.agents],
        }

    def _create_agents(self) -> list[Agent]:
        return AgentFactory(
            config=self.config,
            terrain=self.terrain,
            width=self.width,
            height=self.height,
            restricted_cells=set(self._restricted_cells()),
        ).create_agents(self._rng)

    def _next_movement(self, role: str) -> tuple[int, int]:
        return self.behaviour_profiles.next_movement(role, self._rng)

    def _restricted_cells(self) -> list[tuple[int, int]]:
        mid_x = self.width // 2
        mid_y = self.height // 2
        return [
            (mid_x - 1, mid_y - 1),
            (mid_x, mid_y - 1),
            (mid_x - 1, mid_y),
            (mid_x, mid_y),
        ]

    def _can_enter(
        self, agent: Agent, target_x: int, target_y: int, target_density: int
    ) -> bool:
        cell_type = self._terrain_cell_type(target_x, target_y)
        if self._uses_terrain_enclosure() and not self.terrain.is_inside_simulation_area(target_x, target_y):
            self.metrics.record_boundary_block()
            return False
        if cell_type in (CellType.BOUNDARY, CellType.DENSITY_ZERO):
            self.metrics.record_boundary_block()
            return False
        if cell_type == CellType.RESTRICTED:
            allowed = self.terrain.is_traversable(target_x, target_y, agent.id)
            if not allowed:
                self.metrics.record_restricted_breach(handled=True)
            return allowed
        if cell_type == CellType.GATE:
            allowed = self.terrain.is_traversable(
                target_x, target_y, agent.id, current_density=target_density
            )
            if not allowed:
                self.metrics.record_gate_congestion()
            return allowed
        return True

    def _terrain_cell_type(self, x: int, y: int) -> CellType:
        if x >= self.terrain.width or y >= self.terrain.height:
            return CellType.NORMAL
        return self.terrain.cell_type_at(x, y)

    def _agent_density(self) -> Counter:
        return Counter((agent.position.x, agent.position.y) for agent in self.agents)

    def _uses_default_dimensions(self) -> bool:
        return (
            self.config.terrain_map_path
            and self.config.width == ModelConfig.width
            and self.config.height == ModelConfig.height
        )

    def _uses_terrain_enclosure(self) -> bool:
        return self.width == self.terrain.width and self.height == self.terrain.height

    @staticmethod
    def _clamp(value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, value))
