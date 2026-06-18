## @file analysis.py
#  @brief Simulation analysis collection and report plotting helpers.
#
#  Runs deterministic simulation windows and renders terrain heatmaps,
#  role-specific summaries, congestion curves, exit curves, and replay evidence
#  into one dependency-free HTML report.

from __future__ import annotations

import hashlib
import html
from dataclasses import dataclass, field
from pathlib import Path

from population_model.config import ModelConfig
from population_model.model import PopulationModel

DEFAULT_ANALYSIS_TICKS = 500


@dataclass(frozen=True)
class ReplayEvidence:
    ## @brief Hash evidence proving repeatable simulation state for a seed/tick count.
    first_hash: str
    second_hash: str
    matched: bool

    def to_dict(self) -> dict:
        return {
            "first_hash": self.first_hash,
            "second_hash": self.second_hash,
            "matched": self.matched,
        }


@dataclass
class SimulationAnalysis:
    ## @brief Aggregated report metrics collected from a deterministic model run.
    ticks: int
    terrain_width: int
    terrain_height: int
    terrain_asset_path: str
    heatmap: list[dict[str, int]]
    role_cell_time: dict[str, dict[str, int]]
    role_status_counts: dict[str, dict[str, int]]
    congestion_curve: list[int] = field(default_factory=list)
    exit_curve: list[int] = field(default_factory=list)
    breach_curve: list[int] = field(default_factory=list)
    penalty_curve: list[int] = field(default_factory=list)
    replay: ReplayEvidence | None = None

    def to_dict(self) -> dict:
        return {
            "ticks": self.ticks,
            "terrain_width": self.terrain_width,
            "terrain_height": self.terrain_height,
            "terrain_asset_path": self.terrain_asset_path,
            "heatmap": self.heatmap,
            "role_cell_time": self.role_cell_time,
            "role_status_counts": self.role_status_counts,
            "congestion_curve": self.congestion_curve,
            "exit_curve": self.exit_curve,
            "breach_curve": self.breach_curve,
            "penalty_curve": self.penalty_curve,
            "replay": self.replay.to_dict() if self.replay else None,
        }


def run_analysis(config: ModelConfig, ticks: int = DEFAULT_ANALYSIS_TICKS) -> SimulationAnalysis:
    ## @brief Run a model window and collect report-ready analysis metrics.
    tick_count = max(1, ticks)
    model = PopulationModel(config)
    role_status_counts: dict[str, dict[str, int]] = {}
    congestion_curve: list[int] = []
    exit_curve: list[int] = []
    breach_curve: list[int] = []
    penalty_curve: list[int] = []

    for _ in range(tick_count):
        model.step()
        metrics = model.metrics.to_dict()
        congestion_curve.append(metrics["congestion_count"])
        exit_curve.append(metrics["exit_events"])
        breach_curve.append(metrics["breach_detected"])
        penalty_curve.append(metrics["penalty_cell_traversals"])
        _record_role_status_counts(role_status_counts, model)

    metrics = model.metrics.to_dict()
    first_hash = replay_hash(config, tick_count)
    second_hash = replay_hash(config, tick_count)
    replay = ReplayEvidence(
        first_hash=first_hash,
        second_hash=second_hash,
        matched=first_hash == second_hash,
    )
    return SimulationAnalysis(
        ticks=tick_count,
        terrain_width=model.terrain.width,
        terrain_height=model.terrain.height,
        terrain_asset_path=f"../frontend-react/public/terrain/{model.terrain.source_path.name}",
        heatmap=metrics["cumulative_cell_visits"],
        role_cell_time=metrics["time_spent_by_role"],
        role_status_counts=role_status_counts,
        congestion_curve=congestion_curve,
        exit_curve=exit_curve,
        breach_curve=breach_curve,
        penalty_curve=penalty_curve,
        replay=replay,
    )


def replay_hash(config: ModelConfig, ticks: int) -> str:
    ## @brief Return a stable hash of agent states over a deterministic replay.
    model = PopulationModel(config)
    digest = hashlib.sha256()
    for _ in range(max(1, ticks)):
        model.step()
        for agent in sorted(model.agents, key=lambda item: item.id):
            digest.update(
                (
                    f"{model.tick}|{agent.id}|{agent.role}|{agent.status}|"
                    f"{agent.position.x}|{agent.position.y}|"
                    f"{agent.heading.dx}|{agent.heading.dy};"
                ).encode("utf-8")
            )
    return digest.hexdigest()


def write_analysis_report(analysis: SimulationAnalysis, output: str | Path) -> Path:
    ## @brief Write the complete analysis report HTML artifact.
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_analysis_report(analysis), encoding="utf-8")
    return output_path


def render_analysis_report(analysis: SimulationAnalysis) -> str:
    ## @brief Render all analysis plots into one self-contained HTML document.
    escaped_asset = html.escape(analysis.terrain_asset_path)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Simulation Analysis Report</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; color: #1c2420; background: #f4f6f4; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 24px; }}
    section {{ margin: 0 0 22px; padding: 16px; border: 1px solid #cfd7d0; background: #fff; }}
    h1, h2 {{ margin: 0 0 12px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }}
    .plot {{ width: 100%; height: auto; border: 1px solid #dde4de; background: #fafcfb; }}
    .ok {{ color: #19692c; font-weight: 700; }}
    .bad {{ color: #9b2d1d; font-weight: 700; }}
    code {{ background: #eef2ef; padding: 2px 4px; }}
  </style>
</head>
<body>
<main>
  <h1>Simulation Analysis Report</h1>
  <p>Ticks analysed: <strong>{analysis.ticks}</strong></p>
  <section>
    <h2>Terrain Overlay Heatmap</h2>
    {_render_heatmap(analysis, escaped_asset)}
  </section>
  <div class="grid">
    <section>
      <h2>Role-Specific Cell Time</h2>
      {_render_role_cell_time(analysis)}
    </section>
    <section>
      <h2>Role Status Counts</h2>
      {_render_role_status_counts(analysis)}
    </section>
    <section>
      <h2>Congestion Plot</h2>
      {_render_line_plot(analysis.congestion_curve, "Congested cells")}
    </section>
    <section>
      <h2>Exit Curve</h2>
      {_render_line_plot(analysis.exit_curve, "Cumulative exits")}
    </section>
    <section>
      <h2>Breach / Penalty Curves</h2>
      {_render_dual_line_plot(analysis.breach_curve, analysis.penalty_curve)}
    </section>
    <section>
      <h2>Deterministic Replay Evidence</h2>
      {_render_replay(analysis.replay)}
    </section>
  </div>
</main>
</body>
</html>
"""


def _record_role_status_counts(
    role_status_counts: dict[str, dict[str, int]], model: PopulationModel
) -> None:
    for agent in model.agents:
        role_counts = role_status_counts.setdefault(agent.role, {})
        role_counts[agent.status] = role_counts.get(agent.status, 0) + 1


def _render_heatmap(analysis: SimulationAnalysis, escaped_asset: str) -> str:
    max_count = max((entry["count"] for entry in analysis.heatmap), default=1)
    rects = []
    for entry in analysis.heatmap:
        opacity = max(0.12, min(0.85, entry["count"] / max_count))
        rects.append(
            f'<rect x="{entry["x"]}" y="{entry["y"]}" width="1" height="1" '
            f'fill="#d7191c" opacity="{opacity:.3f}" />'
        )
    return (
        f'<svg class="plot" viewBox="0 0 {analysis.terrain_width} {analysis.terrain_height}" '
        'role="img" aria-label="Terrain heatmap">'
        f'<image href="{escaped_asset}" x="0" y="0" '
        f'width="{analysis.terrain_width}" height="{analysis.terrain_height}" />'
        + "".join(rects)
        + "</svg>"
    )


def _render_role_cell_time(analysis: SimulationAnalysis) -> str:
    rows = []
    for role, cell_times in sorted(analysis.role_cell_time.items()):
        total = max(1, sum(cell_times.values()))
        bars = []
        for cell_type, count in sorted(cell_times.items()):
            width = 100 * count / total
            bars.append(
                f'<div><code>{html.escape(role)} / {html.escape(cell_type)}</code>'
                f'<svg class="plot" viewBox="0 0 100 12">'
                f'<rect x="0" y="1" width="{width:.2f}" height="10" fill="#2d7a46" />'
                f'</svg></div>'
            )
        rows.extend(bars)
    return "".join(rows) or "<p>No role-specific cell time recorded.</p>"


def _render_role_status_counts(analysis: SimulationAnalysis) -> str:
    rows = []
    for role, status_counts in sorted(analysis.role_status_counts.items()):
        total = max(1, sum(status_counts.values()))
        for status, count in sorted(status_counts.items()):
            width = 100 * count / total
            rows.append(
                f'<div><code>{html.escape(role)} / {html.escape(status)}</code>'
                f'<svg class="plot" viewBox="0 0 100 12">'
                f'<rect x="0" y="1" width="{width:.2f}" height="10" fill="#6f5aa8" />'
                f'</svg></div>'
            )
    return "".join(rows) or "<p>No role status counts recorded.</p>"


def _render_line_plot(values: list[int], label: str) -> str:
    return _line_svg([(values, "#255f99", label)])


def _render_dual_line_plot(breaches: list[int], penalties: list[int]) -> str:
    return _line_svg(
        [
            (breaches, "#9b2d1d", "Breaches"),
            (penalties, "#3f48cc", "Penalty traversals"),
        ]
    )


def _line_svg(series: list[tuple[list[int], str, str]]) -> str:
    width = 360
    height = 160
    max_value = max((max(values, default=0) for values, _color, _label in series), default=0)
    max_value = max(1, max_value)
    polylines = []
    labels = []
    for index, (values, color, label) in enumerate(series):
        points = []
        for tick, value in enumerate(values):
            x = 12 + (tick * (width - 24) / max(1, len(values) - 1))
            y = height - 18 - (value * (height - 34) / max_value)
            points.append(f"{x:.2f},{y:.2f}")
        polylines.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="2" '
            f'points="{" ".join(points)}" />'
        )
        labels.append(
            f'<text x="14" y="{16 + index * 14}" font-size="11" fill="{color}">'
            f'{html.escape(label)}</text>'
        )
    return (
        f'<svg class="plot" viewBox="0 0 {width} {height}">'
        f'<line x1="12" y1="{height - 18}" x2="{width - 8}" y2="{height - 18}" stroke="#8b968e" />'
        f'<line x1="12" y1="8" x2="12" y2="{height - 18}" stroke="#8b968e" />'
        + "".join(labels)
        + "".join(polylines)
        + "</svg>"
    )


def _render_replay(replay: ReplayEvidence | None) -> str:
    if replay is None:
        return "<p>No replay evidence recorded.</p>"
    status = "MATCH" if replay.matched else "MISMATCH"
    css_class = "ok" if replay.matched else "bad"
    return (
        f'<p class="{css_class}">{status}</p>'
        f"<p>First hash: <code>{html.escape(replay.first_hash)}</code></p>"
        f"<p>Second hash: <code>{html.escape(replay.second_hash)}</code></p>"
    )
