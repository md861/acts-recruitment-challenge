## @file test_analysis.py
#  @brief Unit tests for simulation analysis report metrics.
#
#  Verifies report aggregation, deterministic replay evidence, and HTML plot
#  generation without requiring external plotting dependencies.

import tempfile
import unittest
from pathlib import Path

from population_model.analysis import run_analysis, write_analysis_report
from population_model.config import ModelConfig


class SimulationAnalysisTests(unittest.TestCase):
    def test_run_analysis_collects_report_metrics(self):
        analysis = run_analysis(
            ModelConfig(width=8, height=6, agent_count=4, seed=3),
            ticks=3,
        )

        self.assertEqual(analysis.ticks, 3)
        self.assertEqual(len(analysis.congestion_curve), 3)
        self.assertEqual(len(analysis.exit_curve), 3)
        self.assertGreater(len(analysis.heatmap), 0)
        self.assertTrue(analysis.role_cell_time)
        self.assertTrue(analysis.role_status_counts)
        self.assertIsNotNone(analysis.replay)
        self.assertTrue(analysis.replay.matched)

    def test_write_analysis_report_contains_expected_plots(self):
        analysis = run_analysis(
            ModelConfig(width=8, height=6, agent_count=4, seed=3),
            ticks=2,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "analysis.html"

            write_analysis_report(analysis, output)

            html = output.read_text()
        self.assertIn("Terrain Overlay Heatmap", html)
        self.assertIn("Role-Specific Cell Time", html)
        self.assertIn("Congestion Plot", html)
        self.assertIn("Exit Curve", html)
        self.assertIn("Deterministic Replay Evidence", html)


if __name__ == "__main__":
    unittest.main()
