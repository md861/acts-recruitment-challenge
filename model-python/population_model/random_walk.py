## @file random_walk.py
#  @brief Configurable random walk movement policies.
#
#  Supports deterministic seeded selection, uniform and weighted choices,
#  wait probability, directional skew, and validation of policy inputs.

import random
from dataclasses import dataclass

Move = tuple[int, int]


@dataclass(frozen=True)
class RandomWalkPolicy:
    moves: tuple[Move, ...]
    weights: tuple[float, ...] | None = None
    wait_probability: float = 0.0
    skew: Move | None = None
    skew_multiplier: float = 1.0

    def choose(self, rng: random.Random) -> Move:
        moves = self._moves_with_optional_wait()
        weights = self._weights_for(moves)
        total = sum(weights)
        if total <= 0:
            raise ValueError("Random walk policy must have positive total weight")

        threshold = rng.random() * total
        running = 0.0
        for move, weight in zip(moves, weights):
            running += weight
            if threshold < running:
                return move
        return moves[-1]

    @classmethod
    def uniform(cls, moves: tuple[Move, ...]) -> "RandomWalkPolicy":
        return cls(moves=moves)

    @classmethod
    def weighted(
        cls, moves: tuple[Move, ...], weights: tuple[float, ...]
    ) -> "RandomWalkPolicy":
        return cls(moves=moves, weights=weights)

    def _moves_with_optional_wait(self) -> tuple[Move, ...]:
        self._validate()
        if self.wait_probability <= 0 or (0, 0) in self.moves:
            return self.moves
        return (*self.moves, (0, 0))

    def _weights_for(self, moves: tuple[Move, ...]) -> tuple[float, ...]:
        if self.weights is None:
            weights = [1.0 for _ in self.moves]
        else:
            weights = list(self.weights)

        if self.wait_probability > 0 and (0, 0) not in self.moves:
            move_total = sum(weights)
            wait_weight = move_total * self.wait_probability / (1 - self.wait_probability)
            weights.append(wait_weight)

        if self.skew is not None and self.skew_multiplier != 1.0:
            weights = [
                weight * self.skew_multiplier if move == self.skew else weight
                for move, weight in zip(moves, weights)
            ]

        return tuple(weights)

    def _validate(self) -> None:
        if not self.moves:
            raise ValueError("Random walk policy must define at least one move")
        if self.weights is not None and len(self.weights) != len(self.moves):
            raise ValueError("Random walk weights must match moves")
        if self.weights is not None and any(weight < 0 for weight in self.weights):
            raise ValueError("Random walk weights cannot be negative")
        if self.wait_probability < 0 or self.wait_probability >= 1:
            raise ValueError("Wait probability must be in the range [0, 1)")
        if self.skew_multiplier < 0:
            raise ValueError("Skew multiplier cannot be negative")
