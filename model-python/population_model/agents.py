## @file agents.py
#  @brief Agent creation and terrain-aware initial placement helpers.
#
#  Provides deterministic role assignment and start-position selection for
#  population model agents.

import random
from dataclasses import dataclass
from typing import Protocol

from population_model.behaviour import DEFAULT_BEHAVIOUR_PROFILES, BehaviourProfileSet
from population_model.config import ModelConfig
from population_model.state import Agent, Heading, Position
from population_model.terrain import CellType


class PlacementTerrain(Protocol):
    width: int
    height: int

    def cell_type_at(self, x: int, y: int) -> CellType:
        ...

    def is_inside_simulation_area(self, x: int, y: int) -> bool:
        ...


@dataclass(frozen=True)
class AgentFactory:
    config: ModelConfig
    terrain: PlacementTerrain
    width: int
    height: int
    restricted_cells: set[tuple[int, int]]
    roles: tuple[str, ...] = ("civilian", "staff", "patrol")
    behaviour_profiles: BehaviourProfileSet = DEFAULT_BEHAVIOUR_PROFILES

    def create_agents(self, rng: random.Random) -> list[Agent]:
        agents: list[Agent] = []
        occupied: set[tuple[int, int]] = set()

        for index in range(self.config.agent_count):
            role = self.roles[index % len(self.roles)]
            behaviour_profile = self.behaviour_profiles.for_role(role)
            position = self.random_free_position(rng, occupied)
            occupied.add((position.x, position.y))
            agents.append(
                Agent(
                    id=f"agent-{index + 1:03d}",
                    role=role,
                    status="waiting",
                    position=position,
                    heading=Heading(dx=0, dy=0),
                    behaviour_profile=behaviour_profile.role,
                )
            )

        return agents

    def random_free_position(
        self, rng: random.Random, occupied: set[tuple[int, int]]
    ) -> Position:
        for _ in range(200):
            position = Position(
                x=rng.randrange(self.width),
                y=rng.randrange(self.height),
            )
            if self.is_available(position, occupied):
                return position

        for y in range(self.height):
            for x in range(self.width):
                position = Position(x=x, y=y)
                if self.is_available(position, occupied):
                    return position

        raise RuntimeError("No terrain-valid free positions are available")

    def is_available(
        self, position: Position, occupied: set[tuple[int, int]]
    ) -> bool:
        key = (position.x, position.y)
        if key in occupied or key in self.restricted_cells:
            return False
        if self._uses_terrain_enclosure() and not self.terrain.is_inside_simulation_area(
            position.x, position.y
        ):
            return False
        cell_type = self._terrain_cell_type(position.x, position.y)
        return cell_type not in (CellType.BOUNDARY, CellType.DENSITY_ZERO)

    def _terrain_cell_type(self, x: int, y: int) -> CellType:
        if x >= self.terrain.width or y >= self.terrain.height:
            return CellType.NORMAL
        return self.terrain.cell_type_at(x, y)

    def _uses_terrain_enclosure(self) -> bool:
        return self.width == self.terrain.width and self.height == self.terrain.height
