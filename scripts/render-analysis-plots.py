#!/usr/bin/env python3
## @file render-analysis-plots.py
#  @brief Generate report-ready simulation analysis plots.
#
#  Produces one dependency-free HTML report containing terrain overlay heatmaps,
#  role-specific metrics, congestion plots, exit curves, and deterministic
#  replay evidence. `SIM_ANALYSIS_TICKS` or `--ticks` controls the simulation
#  window; the default is 500 ticks.

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "model-python"))

from population_model.analysis import DEFAULT_ANALYSIS_TICKS, run_analysis, write_analysis_report
from population_model.config import ModelConfig


def main() -> None:
    args = parse_args()
    config = ModelConfig.from_env()
    report = run_analysis(config, ticks=args.ticks)
    output = write_analysis_report(report, args.output)
    print(output)


def parse_args() -> argparse.Namespace:
    ## @brief Parse analysis tick count and output path.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ticks",
        type=_positive_int,
        default=_env_positive_int("SIM_ANALYSIS_TICKS", DEFAULT_ANALYSIS_TICKS),
        help="Number of simulation ticks to analyse. Defaults to 500.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output HTML report path.",
    )
    args = parser.parse_args()
    if args.output is None:
        args.output = Path(
            os.getenv(
                "SIM_ANALYSIS_OUTPUT",
                str(ROOT / "artifacts" / f"simulation_analysis_{args.ticks}_ticks.html"),
            )
        )
    return args


def _env_positive_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return _positive_int(raw)
    except argparse.ArgumentTypeError:
        return default


def _positive_int(raw: str) -> int:
    value = int(raw)
    if value < 1:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return value


if __name__ == "__main__":
    main()
