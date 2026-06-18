## @file movement.py
#  @brief Terrain-aware movement decision strategy.
#
#  Evaluates proposed moves against terrain enclosure, boundary, restricted
#  cell, gate-density, and penalty-preference rules and returns structured
#  decision metadata.

from dataclasses import dataclass
from typing import Protocol

from population_model.state import Agent
from population_model.terrain import CellType, TerrainPenalty, TerrainTraversal

Move = tuple[int, int]


class MovementTerrain(Protocol):
    width: int
    height: int

    def cell_type_at(self, x: int, y: int) -> CellType:
        ...

    def is_inside_simulation_area(self, x: int, y: int) -> bool:
        ...

    def is_traversable(
        self,
        x: int,
        y: int,
        agent_id: str,
        current_density: int = 0,
        agent_role: str | None = None,
    ) -> bool:
        ...

    def penalty_at(self, x: int, y: int) -> TerrainPenalty | None:
        ...

    def classify_traversal(
        self,
        x: int,
        y: int,
        agent_id: str,
        current_density: int = 0,
        agent_role: str | None = None,
    ) -> TerrainTraversal:
        ...


@dataclass(frozen=True)
class MovementDecision:
    ## @brief Result of evaluating a proposed move.
    move: Move
    target_x: int
    target_y: int
    allowed: bool
    reason: str
    cell_type: CellType
    preference_cost: float = 1.0
    penalty: TerrainPenalty | None = None
    breach_detected: bool = False
    breach_handled: bool = True


@dataclass(frozen=True)
class MovementStrategy:
    ## @brief Apply terrain legality and cost metadata to proposed movement.
    terrain: MovementTerrain
    width: int
    height: int

    def decide(
        self, agent: Agent, move: Move, current_density: int = 0
    ) -> MovementDecision:
        ## @brief Evaluate one candidate move for an agent.
        target_x = self._clamp(agent.position.x + move[0], 0, self.width - 1)
        target_y = self._clamp(agent.position.y + move[1], 0, self.height - 1)
        cell_type = self._terrain_cell_type(target_x, target_y)
        penalty = self._terrain_penalty(target_x, target_y)
        preference_cost = self._preference_cost(move, penalty)

        if self._uses_terrain_enclosure() and not self.terrain.is_inside_simulation_area(
            target_x, target_y
        ):
            return self._blocked(
                move,
                target_x,
                target_y,
                cell_type,
                "outside_enclosure",
                preference_cost,
                penalty,
            )
        if cell_type in (CellType.BOUNDARY, CellType.DENSITY_ZERO):
            return self._blocked(
                move, target_x, target_y, cell_type, "boundary", preference_cost, penalty
            )
        if cell_type == CellType.RESTRICTED:
            traversal = self.terrain.classify_traversal(
                target_x,
                target_y,
                agent.id,
                agent_role=agent.role,
            )
            if not traversal.allowed:
                return self._blocked(
                    move,
                    target_x,
                    target_y,
                    cell_type,
                    traversal.reason,
                    preference_cost,
                    penalty,
                    breach_detected=traversal.breach_detected,
                    breach_handled=traversal.breach_handled,
                )
        if cell_type == CellType.GATE:
            traversal = self.terrain.classify_traversal(
                target_x,
                target_y,
                agent.id,
                current_density=current_density,
                agent_role=agent.role,
            )
            if not traversal.allowed:
                return self._blocked(
                    move,
                    target_x,
                    target_y,
                    cell_type,
                    traversal.reason,
                    preference_cost,
                    penalty,
                )

        return MovementDecision(
            move=move,
            target_x=target_x,
            target_y=target_y,
            allowed=True,
            reason="allowed",
            cell_type=cell_type,
            preference_cost=preference_cost,
            penalty=penalty,
        )

    def _blocked(
        self,
        move: Move,
        target_x: int,
        target_y: int,
        cell_type: CellType,
        reason: str,
        preference_cost: float,
        penalty: TerrainPenalty | None,
        breach_detected: bool = False,
        breach_handled: bool = True,
    ) -> MovementDecision:
        return MovementDecision(
            move=move,
            target_x=target_x,
            target_y=target_y,
            allowed=False,
            reason=reason,
            cell_type=cell_type,
            preference_cost=preference_cost,
            penalty=penalty,
            breach_detected=breach_detected,
            breach_handled=breach_handled,
        )

    def _terrain_cell_type(self, x: int, y: int) -> CellType:
        if x >= self.terrain.width or y >= self.terrain.height:
            return CellType.NORMAL
        return self.terrain.cell_type_at(x, y)

    def _terrain_penalty(self, x: int, y: int) -> TerrainPenalty | None:
        if x >= self.terrain.width or y >= self.terrain.height:
            return None
        return self.terrain.penalty_at(x, y)

    def _preference_cost(
        self, move: Move, penalty: TerrainPenalty | None
    ) -> float:
        if penalty is None:
            return 1.0
        if penalty.kind == "type_1":
            return self._type_1_penalty_cost(move, penalty)
        if penalty.kind == "type_2":
            return 1.0 / max(penalty.multiplier or 1.0, 0.01)
        return 1.0

    def _type_1_penalty_cost(self, move: Move, penalty: TerrainPenalty) -> float:
        multiplier = max(penalty.multiplier or 1.0, 0.01)
        if penalty.direction is None or self._direction_for(move) == penalty.direction:
            return 1.0 / multiplier
        return 1.0

    def _direction_for(self, move: Move) -> str | None:
        return {
            (1, 0): "east",
            (-1, 0): "west",
            (0, -1): "north",
            (0, 1): "south",
            (0, 0): "wait",
        }.get(move)

    def _uses_terrain_enclosure(self) -> bool:
        return self.width == self.terrain.width and self.height == self.terrain.height

    @staticmethod
    def _clamp(value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, value))
