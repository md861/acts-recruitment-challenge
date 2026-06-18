import random
import unittest

from population_model.behaviour import (
    DEFAULT_BEHAVIOUR_PROFILES,
    BehaviourProfile,
    BehaviourProfileSet,
)
from population_model.terrain import CellType


class BehaviourProfileTests(unittest.TestCase):
    def test_default_profiles_expose_role_specific_intent(self):
        civilian = DEFAULT_BEHAVIOUR_PROFILES.for_role("civilian")
        staff = DEFAULT_BEHAVIOUR_PROFILES.for_role("staff")
        patrol = DEFAULT_BEHAVIOUR_PROFILES.for_role("patrol")

        self.assertIn((0, 0), civilian.candidate_moves)
        self.assertIn(CellType.RESTRICTED, civilian.avoid_cell_types)
        self.assertIn((0, 0), staff.candidate_moves)
        self.assertIn(CellType.TYPE_1_PENALTY, staff.avoid_cell_types)
        self.assertNotIn((0, 0), patrol.candidate_moves)
        self.assertTrue(patrol.may_enter_restricted)

    def test_movement_selection_is_deterministic_for_seed(self):
        first_rng = random.Random(12)
        second_rng = random.Random(12)

        first = [
            DEFAULT_BEHAVIOUR_PROFILES.next_movement("civilian", first_rng)
            for _ in range(10)
        ]
        second = [
            DEFAULT_BEHAVIOUR_PROFILES.next_movement("civilian", second_rng)
            for _ in range(10)
        ]

        self.assertEqual(first, second)

    def test_unknown_roles_use_default_profile(self):
        profile_set = BehaviourProfileSet(
            profiles={
                "civilian": BehaviourProfile(
                    role="civilian",
                    candidate_moves=((0, 0),),
                )
            }
        )

        self.assertEqual(
            profile_set.next_movement("visitor", random.Random(1)),
            (0, 0),
        )

    def test_empty_profile_is_rejected_when_selected(self):
        profile = BehaviourProfile(role="broken", candidate_moves=())

        with self.assertRaises(ValueError):
            profile.choose_next_move(random.Random(1))


if __name__ == "__main__":
    unittest.main()
