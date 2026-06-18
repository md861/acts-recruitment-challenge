import random
import unittest

from population_model.random_walk import RandomWalkPolicy


class RandomWalkPolicyTests(unittest.TestCase):
    def test_uniform_policy_is_deterministic_for_seed(self):
        policy = RandomWalkPolicy.uniform(((-1, 0), (1, 0), (0, 1)))
        first_rng = random.Random(8)
        second_rng = random.Random(8)

        first = [policy.choose(first_rng) for _ in range(12)]
        second = [policy.choose(second_rng) for _ in range(12)]

        self.assertEqual(first, second)

    def test_weighted_policy_prefers_positive_weighted_move(self):
        policy = RandomWalkPolicy.weighted(
            moves=((-1, 0), (1, 0), (0, 1)),
            weights=(0.0, 10.0, 0.0),
        )

        choices = {policy.choose(random.Random(seed)) for seed in range(10)}

        self.assertEqual(choices, {(1, 0)})

    def test_wait_probability_adds_wait_move(self):
        policy = RandomWalkPolicy(
            moves=((1, 0),),
            wait_probability=0.5,
        )

        choices = {policy.choose(random.Random(seed)) for seed in range(20)}

        self.assertEqual(choices, {(1, 0), (0, 0)})

    def test_skew_multiplier_increases_matching_move_weight(self):
        policy = RandomWalkPolicy(
            moves=((-1, 0), (1, 0)),
            skew=(1, 0),
            skew_multiplier=100.0,
        )

        choices = [policy.choose(random.Random(seed)) for seed in range(20)]

        self.assertGreater(choices.count((1, 0)), choices.count((-1, 0)))

    def test_invalid_policy_rejects_empty_moves(self):
        policy = RandomWalkPolicy.uniform(())

        with self.assertRaises(ValueError):
            policy.choose(random.Random(1))

    def test_invalid_policy_rejects_weight_mismatch(self):
        policy = RandomWalkPolicy.weighted(((1, 0),), (1.0, 2.0))

        with self.assertRaises(ValueError):
            policy.choose(random.Random(1))

    def test_invalid_policy_rejects_bad_wait_probability(self):
        policy = RandomWalkPolicy(moves=((1, 0),), wait_probability=1.0)

        with self.assertRaises(ValueError):
            policy.choose(random.Random(1))


if __name__ == "__main__":
    unittest.main()
