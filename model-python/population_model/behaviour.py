## @file behaviour.py
#  @brief Role-specific behaviour profiles for movement intent.
#
#  Connects agent roles to random walk policies and terrain preference
#  metadata used by movement orchestration.

import random
from collections.abc import Mapping
from dataclasses import dataclass

from population_model.movement import MovementDecision, MovementStrategy
from population_model.random_walk import RandomWalkPolicy
from population_model.state import Agent
from population_model.terrain import CellType

Move = tuple[int, int]


@dataclass(frozen=True)
class BehaviourProfile:
    ## @brief Role-level movement intent and random walk policy.
    #
    #  A profile describes candidate movement choices, terrain cell types the
    #  role should avoid when alternatives exist, and whether restricted-cell
    #  movement should remain a valid intent.
    role: str
    random_walk: RandomWalkPolicy
    avoid_cell_types: tuple[CellType, ...] = ()
    may_enter_restricted: bool = False

    @property
    def candidate_moves(self) -> tuple[Move, ...]:
        return self.random_walk.moves

    def choose_next_move(self, rng: random.Random) -> Move:
        ## @brief Choose a movement from the profile's full candidate set.
        return self.choose_from(self.candidate_moves, rng)

    def choose_from(self, candidate_moves: tuple[Move, ...], rng: random.Random) -> Move:
        ## @brief Choose from a filtered candidate move set.
        #
        #  Preserves the profile's weighting, skew, and seeded determinism while
        #  allowing selectors to remove blocked or behaviour-avoided moves.
        try:
            return self.random_walk.with_moves(candidate_moves).choose(rng)
        except ValueError as exc:
            raise ValueError(f"Invalid behaviour profile for {self.role}") from exc

    def choose_from_decisions(
        self, decisions: tuple[MovementDecision, ...], rng: random.Random
    ) -> MovementDecision:
        ## @brief Choose a movement decision using the profile's random walk policy.
        moves = tuple(decision.move for decision in decisions)
        selected_move = self.choose_from(moves, rng)
        for decision in decisions:
            if decision.move == selected_move:
                return decision
        return decisions[-1]


@dataclass(frozen=True)
class BehaviourProfileSet:
    ## @brief Lookup table for role-specific behaviour profiles.
    profiles: Mapping[str, BehaviourProfile]
    default_role: str = "civilian"

    def for_role(self, role: str) -> BehaviourProfile:
        try:
            return self.profiles[role]
        except KeyError:
            return self.profiles[self.default_role]

    def next_movement(self, role: str, rng: random.Random) -> Move:
        return self.for_role(role).choose_next_move(rng)


@dataclass(frozen=True)
class BehaviourMoveSelector:
    ## @brief Select behaviour-aware movement decisions for agents.
    #
    #  Evaluates each role profile's candidate moves through the movement
    #  strategy, prefers allowed moves, filters avoidable terrain when possible,
    #  and falls back deterministically when every candidate is blocked.
    profiles: BehaviourProfileSet
    movement_strategy: MovementStrategy

    def select(
        self,
        agent: Agent,
        rng: random.Random,
        current_density_by_target: Mapping[Move, int],
    ) -> MovementDecision:
        ## @brief Return the selected movement decision for one agent.
        profile = self.profiles.for_role(agent.role)
        decisions = tuple(
            self.movement_strategy.decide(
                agent,
                move,
                current_density=current_density_by_target.get(move, 0),
            )
            for move in profile.candidate_moves
        )
        allowed = tuple(decision for decision in decisions if decision.allowed)
        if not allowed:
            return profile.choose_from_decisions(decisions, rng)

        preferred_without_avoided = tuple(
            decision
            for decision in allowed
            if self._is_preferred(profile, decision.cell_type)
        )
        preferred = self._lowest_cost(preferred_without_avoided or allowed)
        return profile.choose_from_decisions(preferred, rng)

    def _is_preferred(self, profile: BehaviourProfile, cell_type: CellType) -> bool:
        if profile.may_enter_restricted and cell_type == CellType.RESTRICTED:
            return True
        return cell_type not in profile.avoid_cell_types

    def _lowest_cost(
        self, decisions: tuple[MovementDecision, ...]
    ) -> tuple[MovementDecision, ...]:
        lowest = min(decision.preference_cost for decision in decisions)
        return tuple(
            decision for decision in decisions if decision.preference_cost == lowest
        )


DEFAULT_BEHAVIOUR_PROFILES = BehaviourProfileSet(
    profiles={
        "civilian": BehaviourProfile(
            role="civilian",
            random_walk=RandomWalkPolicy.uniform(
                ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))
            ),
            avoid_cell_types=(
                CellType.RESTRICTED,
                CellType.TYPE_1_PENALTY,
                CellType.TYPE_2_PENALTY,
            ),
        ),
        "staff": BehaviourProfile(
            role="staff",
            random_walk=RandomWalkPolicy.weighted(
                ((0, 0), (1, 0), (0, 1), (-1, 0)),
                (2.0, 1.0, 1.0, 1.0),
            ),
            avoid_cell_types=(CellType.TYPE_1_PENALTY, CellType.TYPE_2_PENALTY),
        ),
        "patrol": BehaviourProfile(
            role="patrol",
            random_walk=RandomWalkPolicy.uniform(
                ((-1, 0), (1, 0), (0, -1), (0, 1))
            ),
            may_enter_restricted=True,
        ),
    }
)
