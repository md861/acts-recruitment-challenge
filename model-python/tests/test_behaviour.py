import random
import unittest

from population_model.behaviour import (
    BehaviourMoveSelector,
    DEFAULT_BEHAVIOUR_PROFILES,
    BehaviourProfile,
    BehaviourProfileSet,
)
from population_model.movement import MovementStrategy
from population_model.random_walk import RandomWalkPolicy
from population_model.state import Agent, Heading, Position
from population_model.terrain import CellType, TerrainCell, TerrainPenalty, TerrainTraversal


class StubTerrain:
    def __init__(
        self,
        cells=None,
        penalties=None,
        allowed_restricted_ids=("agent-patrol",),
    ):
        self.width = 3
        self.height = 3
        self.cells = cells or {}
        self.penalties = penalties or {}
        self.allowed_restricted_ids = allowed_restricted_ids

    def cell_type_at(self, x, y):
        return self.cells.get((x, y), CellType.NORMAL)

    def is_inside_simulation_area(self, x, y):
        return True

    def is_traversable(self, x, y, agent_id, current_density=0, agent_role=None):
        cell_type = self.cell_type_at(x, y)
        if cell_type == CellType.RESTRICTED:
            return agent_id in self.allowed_restricted_ids or agent_role == "patrol"
        return cell_type not in (CellType.BOUNDARY, CellType.DENSITY_ZERO)

    def penalty_at(self, x, y):
        return self.penalties.get((x, y))

    def classify_traversal(
        self, x, y, agent_id, current_density=0, agent_role=None
    ):
        cell_type = self.cell_type_at(x, y)
        cell = TerrainCell(x=x, y=y, cell_type=cell_type)
        if cell_type in (CellType.BOUNDARY, CellType.DENSITY_ZERO):
            return TerrainTraversal(False, "boundary", cell)
        if cell_type == CellType.RESTRICTED and not self.is_traversable(
            x, y, agent_id, current_density, agent_role
        ):
            return TerrainTraversal(
                False,
                "restricted",
                cell,
                breach_detected=True,
            )
        return TerrainTraversal(True, "allowed", cell)


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
                    random_walk=RandomWalkPolicy.uniform(((0, 0),)),
                )
            }
        )

        self.assertEqual(
            profile_set.next_movement("visitor", random.Random(1)),
            (0, 0),
        )

    def test_empty_profile_is_rejected_when_selected(self):
        profile = BehaviourProfile(
            role="broken",
            random_walk=RandomWalkPolicy.uniform(()),
        )

        with self.assertRaises(ValueError):
            profile.choose_next_move(random.Random(1))

    def test_civilian_avoids_restricted_and_penalty_cells_when_possible(self):
        selector = self._selector(
            BehaviourProfile(
                role="civilian",
                random_walk=RandomWalkPolicy.uniform(((1, 0), (0, 1), (0, 0))),
                avoid_cell_types=(
                    CellType.RESTRICTED,
                    CellType.TYPE_1_PENALTY,
                    CellType.TYPE_2_PENALTY,
                ),
            ),
            cells={
                (2, 1): CellType.RESTRICTED,
                (1, 2): CellType.TYPE_1_PENALTY,
            },
        )

        decision = selector.select(
            self._agent(role="civilian"),
            random.Random(1),
            current_density_by_target={},
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.move, (0, 0))
        self.assertEqual(decision.cell_type, CellType.NORMAL)

    def test_staff_prefers_waiting_over_penalty_cells(self):
        selector = self._selector(
            BehaviourProfile(
                role="staff",
                random_walk=RandomWalkPolicy.weighted(
                    ((0, 0), (1, 0)),
                    (3.0, 1.0),
                ),
                avoid_cell_types=(CellType.TYPE_1_PENALTY,),
            ),
            cells={(2, 1): CellType.TYPE_1_PENALTY},
        )

        decision = selector.select(
            self._agent(role="staff"),
            random.Random(2),
            current_density_by_target={},
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.move, (0, 0))

    def test_patrol_can_choose_allowed_restricted_cells(self):
        selector = self._selector(
            BehaviourProfile(
                role="patrol",
                random_walk=RandomWalkPolicy.weighted(
                    ((1, 0), (0, 0)),
                    (10.0, 0.0),
                ),
                may_enter_restricted=True,
            ),
            cells={(2, 1): CellType.RESTRICTED},
        )

        decision = selector.select(
            self._agent(agent_id="agent-patrol", role="patrol"),
            random.Random(3),
            current_density_by_target={},
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.move, (1, 0))
        self.assertEqual(decision.cell_type, CellType.RESTRICTED)

    def test_selector_returns_blocked_decision_when_all_candidates_are_blocked(self):
        selector = self._selector(
            BehaviourProfile(
                role="civilian",
                random_walk=RandomWalkPolicy.uniform(((1, 0), (0, 1))),
            ),
            cells={
                (2, 1): CellType.BOUNDARY,
                (1, 2): CellType.DENSITY_ZERO,
            },
        )

        decision = selector.select(
            self._agent(role="civilian"),
            random.Random(4),
            current_density_by_target={},
        )

        self.assertFalse(decision.allowed)
        self.assertIn(decision.reason, ("boundary", "outside_enclosure"))

    def test_selector_prefers_lower_cost_allowed_moves(self):
        selector = self._selector(
            BehaviourProfile(
                role="civilian",
                random_walk=RandomWalkPolicy.uniform(((1, 0), (0, 0))),
            ),
            cells={(2, 1): CellType.TYPE_1_PENALTY},
            penalties={
                (2, 1): TerrainPenalty(
                    kind="type_1",
                    direction="east",
                    multiplier=0.5,
                )
            },
        )

        decision = selector.select(
            self._agent(role="civilian"),
            random.Random(1),
            current_density_by_target={},
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.move, (0, 0))
        self.assertLess(decision.preference_cost, 2.0)

    def _selector(self, profile, cells, penalties=None):
        terrain = StubTerrain(cells=cells, penalties=penalties)
        profile_set = BehaviourProfileSet(
            profiles={profile.role: profile},
            default_role=profile.role,
        )
        return BehaviourMoveSelector(
            profiles=profile_set,
            movement_strategy=MovementStrategy(terrain=terrain, width=3, height=3),
        )

    def _agent(self, agent_id="agent-001", role="civilian"):
        return Agent(
            id=agent_id,
            role=role,
            status="waiting",
            position=Position(x=1, y=1),
            heading=Heading(dx=0, dy=0),
        )


if __name__ == "__main__":
    unittest.main()
