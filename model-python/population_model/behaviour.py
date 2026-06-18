## @file behaviour.py
#  @brief Role-specific behaviour profiles for movement intent.
#
#  Connects agent roles to random walk policies and terrain preference
#  metadata used by movement orchestration.

import random
from collections.abc import Mapping
from dataclasses import dataclass

from population_model.random_walk import RandomWalkPolicy
from population_model.terrain import CellType

Move = tuple[int, int]


@dataclass(frozen=True)
class BehaviourProfile:
    role: str
    random_walk: RandomWalkPolicy
    avoid_cell_types: tuple[CellType, ...] = ()
    may_enter_restricted: bool = False

    @property
    def candidate_moves(self) -> tuple[Move, ...]:
        return self.random_walk.moves

    def choose_next_move(self, rng: random.Random) -> Move:
        try:
            return self.random_walk.choose(rng)
        except ValueError as exc:
            raise ValueError(f"Invalid behaviour profile for {self.role}") from exc


@dataclass(frozen=True)
class BehaviourProfileSet:
    profiles: Mapping[str, BehaviourProfile]
    default_role: str = "civilian"

    def for_role(self, role: str) -> BehaviourProfile:
        try:
            return self.profiles[role]
        except KeyError:
            return self.profiles[self.default_role]

    def next_movement(self, role: str, rng: random.Random) -> Move:
        return self.for_role(role).choose_next_move(rng)


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
