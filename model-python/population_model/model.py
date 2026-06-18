## @file model.py
#  @brief Population model orchestration and snapshot construction.
#
#  Coordinates configuration, terrain, agent creation, behaviour, movement,
#  metrics, tick progression, reset behaviour, and public snapshots.

import random
from collections import Counter
from datetime import datetime, timezone

from population_model.agents import AgentFactory
from population_model.behaviour import (
    BehaviourMoveSelector,
    DEFAULT_BEHAVIOUR_PROFILES,
    BehaviourProfileSet,
)
from population_model.config import ModelConfig
from population_model.metrics import TerrainMetrics
from population_model.movement import MovementDecision, MovementStrategy
from population_model.state import Agent, Heading, Position
from population_model.terrain import CellType, load_terrain_map


class PopulationModel:
    """A deliberately simple population model.

    The model coordinates deterministic agent creation, terrain-aware movement,
    behaviour profile selection, metric accumulation, and public snapshots.
    """

    def __init__(self, config: ModelConfig):
        self.config = config
        self.terrain = load_terrain_map(config)
        self.width = self.terrain.width if self._uses_default_dimensions() else config.width
        self.height = self.terrain.height if self._uses_default_dimensions() else config.height
        self.behaviour_profiles: BehaviourProfileSet = DEFAULT_BEHAVIOUR_PROFILES
        self._reset_runtime_state()

    def reset(self) -> None:
        self._reset_runtime_state()

    def step(self, ticks: int = 1) -> None:
        for _ in range(max(1, ticks)):
            self._advance_tick()

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

    def _reset_runtime_state(self) -> None:
        self._rng = random.Random(self.config.seed)
        self.metrics = TerrainMetrics()
        self.movement_strategy = self._create_movement_strategy()
        self.behaviour_selector = self._create_behaviour_selector()
        self.tick = 0
        self.agents = self._create_agents()
        self._record_density_snapshot()

    def _advance_tick(self) -> None:
        self.tick += 1
        density = self._agent_density()
        for agent in self.agents:
            self._advance_agent(agent, density)
        self._record_density_snapshot(density)

    def _advance_agent(self, agent: Agent, density: Counter) -> None:
        current_key = self._agent_position_key(agent)
        decision = self._select_movement(agent, density)
        self._apply_movement_decision(agent, decision)
        self._record_agent_cell_time(agent)
        self._update_density(density, current_key, self._agent_position_key(agent))

    def _apply_movement_decision(
        self, agent: Agent, decision: MovementDecision
    ) -> None:
        agent.heading = Heading(dx=decision.move[0], dy=decision.move[1])
        if decision.allowed:
            self._apply_allowed_movement(agent, decision)
        else:
            self._record_blocked_movement(decision)
            agent.status = "blocked"

    def _apply_allowed_movement(
        self, agent: Agent, decision: MovementDecision
    ) -> None:
        agent.position.x = decision.target_x
        agent.position.y = decision.target_y
        self._record_allowed_movement(decision, agent.id)
        agent.status = "waiting" if decision.move == (0, 0) else "moving"

    def _create_agents(self) -> list[Agent]:
        return AgentFactory(
            config=self.config,
            terrain=self.terrain,
            width=self.width,
            height=self.height,
            restricted_cells=set(self._restricted_cells()),
            behaviour_profiles=self.behaviour_profiles,
        ).create_agents(self._rng)

    def _create_movement_strategy(self) -> MovementStrategy:
        return MovementStrategy(
            terrain=self.terrain,
            width=self.width,
            height=self.height,
        )

    def _create_behaviour_selector(self) -> BehaviourMoveSelector:
        return BehaviourMoveSelector(
            profiles=self.behaviour_profiles,
            movement_strategy=self.movement_strategy,
        )

    def _next_movement(self, role: str) -> tuple[int, int]:
        return self.behaviour_profiles.next_movement(role, self._rng)

    def _select_movement(self, agent: Agent, density: Counter) -> MovementDecision:
        overridden_next_movement = self.__dict__.get("_next_movement")
        if overridden_next_movement is not None:
            return self._movement_decision(
                agent,
                overridden_next_movement(agent.role),
                density,
            )
        return self.behaviour_selector.select(
            agent,
            self._rng,
            self._current_density_by_candidate_move(agent, density),
        )

    def _movement_decision(
        self, agent: Agent, move: tuple[int, int], density: Counter
    ) -> MovementDecision:
        target_x = self._clamp(agent.position.x + move[0], 0, self.width - 1)
        target_y = self._clamp(agent.position.y + move[1], 0, self.height - 1)
        target_key = (target_x, target_y)
        current_key = (agent.position.x, agent.position.y)
        target_density = density.get(target_key, 0)
        if target_key == current_key:
            target_density = max(0, target_density - 1)
        return self.movement_strategy.decide(
            agent, move, current_density=target_density
        )

    def _current_density_by_candidate_move(
        self, agent: Agent, density: Counter
    ) -> dict[tuple[int, int], int]:
        profile = self.behaviour_profiles.for_role(agent.role)
        current_key = (agent.position.x, agent.position.y)
        densities: dict[tuple[int, int], int] = {}
        for move in profile.candidate_moves:
            target_x = self._clamp(agent.position.x + move[0], 0, self.width - 1)
            target_y = self._clamp(agent.position.y + move[1], 0, self.height - 1)
            target_key = (target_x, target_y)
            target_density = density.get(target_key, 0)
            if target_key == current_key:
                target_density = max(0, target_density - 1)
            densities[move] = target_density
        return densities

    def _record_blocked_movement(self, decision: MovementDecision) -> None:
        if decision.reason in ("outside_enclosure", "boundary"):
            self.metrics.record_boundary_block()
        elif decision.reason == "restricted":
            self.metrics.record_restricted_breach(handled=decision.breach_handled)
        elif decision.reason == "gate_congestion":
            self.metrics.record_gate_congestion()

    def _record_allowed_movement(
        self, decision: MovementDecision, agent_id: str
    ) -> None:
        if decision.cell_type in (
            CellType.TYPE_1_PENALTY,
            CellType.TYPE_2_PENALTY,
        ):
            self.metrics.record_penalty_traversal()
        if self.terrain.is_exit_cell(decision.target_x, decision.target_y, agent_id):
            self.metrics.record_exit()

    def _record_agent_cell_time(self, agent: Agent) -> None:
        self.metrics.record_cell_time(
            agent.id,
            self._terrain_cell_type(agent.position.x, agent.position.y),
            role=agent.role,
        )

    def _record_density_snapshot(self, density: Counter | None = None) -> None:
        self.metrics.record_density(density or self._agent_density())

    def _update_density(
        self,
        density: Counter,
        previous_key: tuple[int, int],
        current_key: tuple[int, int],
    ) -> None:
        density[previous_key] = max(0, density.get(previous_key, 0) - 1)
        density[current_key] = density.get(current_key, 0) + 1

    def _agent_position_key(self, agent: Agent) -> tuple[int, int]:
        return (agent.position.x, agent.position.y)

    def _restricted_cells(self) -> list[tuple[int, int]]:
        mid_x = self.width // 2
        mid_y = self.height // 2
        return [
            (mid_x - 1, mid_y - 1),
            (mid_x, mid_y - 1),
            (mid_x - 1, mid_y),
            (mid_x, mid_y),
        ]

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

    @staticmethod
    def _clamp(value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(maximum, value))
