from dataclasses import dataclass
from typing import Protocol

from population_model.state import Agent
from population_model.terrain import CellType

Move = tuple[int, int]


class MovementTerrain(Protocol):
    width: int
    height: int

    def cell_type_at(self, x: int, y: int) -> CellType:
        ...

    def is_inside_simulation_area(self, x: int, y: int) -> bool:
        ...

    def is_traversable(
        self, x: int, y: int, agent_id: str, current_density: int = 0
    ) -> bool:
        ...


@dataclass(frozen=True)
class MovementDecision:
    move: Move
    target_x: int
    target_y: int
    allowed: bool
    reason: str
    cell_type: CellType


@dataclass(frozen=True)
class MovementStrategy:
    terrain: MovementTerrain
    width: int
    height: int

    def decide(
        self, agent: Agent, move: Move, current_density: int = 0
    ) -> MovementDecision:
        target_x = self._clamp(agent.position.x + move[0], 0, self.width - 1)
        target_y = self._clamp(agent.position.y + move[1], 0, self.height - 1)
        cell_type = self._terrain_cell_type(target_x, target_y)

        if self._uses_terrain_enclosure() and not self.terrain.is_inside_simulation_area(
            target_x, target_y
        ):
            return self._blocked(move, target_x, target_y, cell_type, "outside_enclosure")
        if cell_type in (CellType.BOUNDARY, CellType.DENSITY_ZERO):
            return self._blocked(move, target_x, target_y, cell_type, "boundary")
        if cell_type == CellType.RESTRICTED:
            allowed = self.terrain.is_traversable(target_x, target_y, agent.id)
            if not allowed:
                return self._blocked(move, target_x, target_y, cell_type, "restricted")
        if cell_type == CellType.GATE:
            allowed = self.terrain.is_traversable(
                target_x,
                target_y,
                agent.id,
                current_density=current_density,
            )
            if not allowed:
                return self._blocked(
                    move, target_x, target_y, cell_type, "gate_congestion"
                )

        return MovementDecision(
            move=move,
            target_x=target_x,
            target_y=target_y,
            allowed=True,
            reason="allowed",
            cell_type=cell_type,
        )

    def _blocked(
        self,
        move: Move,
        target_x: int,
        target_y: int,
        cell_type: CellType,
        reason: str,
    ) -> MovementDecision:
        return MovementDecision(
            move=move,
            target_x=target_x,
            target_y=target_y,
            allowed=False,
            reason=reason,
            cell_type=cell_type,
        )

    def _terrain_cell_type(self, x: int, y: int) -> CellType:
        if x >= self.terrain.width or y >= self.terrain.height:
            return CellType.NORMAL
        return self.terrain.cell_type_at(x, y)

    def _uses_terrain_enclosure(self) -> bool:
        return self.width == self.terrain.width and self.height == self.terrain.height

    @staticmethod
    def _clamp(value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, value))
