## @file test_metrics.py
#  @brief Unit tests for terrain-aware metric accumulation.
#
#  Verifies density snapshots, congestion summaries, breach accounting, penalty
#  events, exits, blocked movement counts, and time-spent serialization without
#  depending on full model orchestration.

import unittest

from population_model.metrics import TerrainMetrics
from population_model.terrain import CellType


class TerrainMetricsTests(unittest.TestCase):
    def test_records_cell_density_and_congested_cells(self):
        metrics = TerrainMetrics()

        metrics.record_density(
            {
                (2, 3): 1,
                (1, 1): 3,
                (0, 0): 0,
                (4, 5): 2,
            },
            congestion_threshold=2,
        )

        payload = metrics.to_dict()
        self.assertEqual(
            payload["cell_density"],
            [
                {"x": 1, "y": 1, "count": 3},
                {"x": 2, "y": 3, "count": 1},
                {"x": 4, "y": 5, "count": 2},
            ],
        )
        self.assertEqual(payload["congestion_count"], 2)
        self.assertEqual(
            payload["congested_cells"],
            [
                {"x": 1, "y": 1, "count": 3},
                {"x": 4, "y": 5, "count": 2},
            ],
        )

    def test_records_handled_and_unresolved_breaches(self):
        metrics = TerrainMetrics()

        metrics.record_restricted_breach(handled=True)
        metrics.record_restricted_breach(handled=False)

        payload = metrics.to_dict()
        self.assertEqual(payload["breach_detected"], 2)
        self.assertEqual(payload["breach_handled"], 1)
        self.assertEqual(payload["unresolved_breaches"], 1)

    def test_records_event_counters_and_time_spent_by_cell_type(self):
        metrics = TerrainMetrics()

        metrics.record_boundary_block()
        metrics.record_gate_congestion()
        metrics.record_exit()
        metrics.record_penalty_traversal()
        metrics.record_cell_time("agent-001", CellType.NORMAL)
        metrics.record_cell_time("agent-001", CellType.TYPE_1_PENALTY)
        metrics.record_cell_time("agent-001", CellType.TYPE_1_PENALTY)

        payload = metrics.to_dict()
        self.assertEqual(payload["blocked_boundary_attempts"], 1)
        self.assertEqual(payload["gate_congestion_events"], 1)
        self.assertEqual(payload["exit_events"], 1)
        self.assertEqual(payload["penalty_cell_traversals"], 1)
        self.assertEqual(
            payload["time_spent_by_agent_id"]["agent-001"],
            {"normal": 1, "type_1_penalty": 2},
        )


if __name__ == "__main__":
    unittest.main()
