import random
from collections.abc import Mapping
from dataclasses import dataclass

from population_model.terrain import CellType

Move = tuple[int, int]


@dataclass(frozen=True)
class BehaviourProfile:
    role: str
    candidate_moves: tuple[Move, ...]
    avoid_cell_types: tuple[CellType, ...] = ()
    may_enter_restricted: bool = False

    def choose_next_move(self, rng: random.Random) -> Move:
        if not self.candidate_moves:
            raise ValueError(f"Behaviour profile for {self.role} has no moves")
        return rng.choice(self.candidate_moves)


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
            candidate_moves=((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)),
            avoid_cell_types=(
                CellType.RESTRICTED,
                CellType.TYPE_1_PENALTY,
                CellType.TYPE_2_PENALTY,
            ),
        ),
        "staff": BehaviourProfile(
            role="staff",
            candidate_moves=((0, 0), (1, 0), (0, 1), (-1, 0)),
            avoid_cell_types=(CellType.TYPE_1_PENALTY, CellType.TYPE_2_PENALTY),
        ),
        "patrol": BehaviourProfile(
            role="patrol",
            candidate_moves=((-1, 0), (1, 0), (0, -1), (0, 1)),
            may_enter_restricted=True,
        ),
    }
)
