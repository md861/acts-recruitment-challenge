## @file metrics.py
#  @brief Terrain-aware simulation metric accumulation.
#
#  Tracks cell density, congested cells, movement blocks, breach handling, gate
#  congestion, exits, penalty traversals, and per-agent time spent by terrain
#  cell type.

from collections import defaultdict
from dataclasses import dataclass, field

from population_model.terrain import CellType

CellKey = tuple[int, int]


@dataclass
class TerrainMetrics:
    ## @brief Accumulate terrain-related observations for snapshots and tests.
    #
    #  The metrics object deliberately stays policy-free: model orchestration
    #  reports density snapshots and movement outcomes, while this class derives
    #  congestion summaries, unresolved breach counts, and serializable payloads.
    breach_detected: int = 0
    breach_handled: int = 0
    blocked_boundary_attempts: int = 0
    gate_congestion_events: int = 0
    exit_events: int = 0
    penalty_cell_traversals: int = 0
    cell_density: dict[CellKey, int] = field(default_factory=dict)
    congestion_count: int = 0
    congested_cells: list[dict[str, int]] = field(default_factory=list)
    time_spent_by_agent_id: dict[str, dict[str, int]] = field(default_factory=dict)

    @property
    def unresolved_breaches(self) -> int:
        return max(0, self.breach_detected - self.breach_handled)

    def record_density(
        self, density: dict[CellKey, int], congestion_threshold: int = 2
    ) -> None:
        threshold = max(1, congestion_threshold)
        self.cell_density = {
            key: count for key, count in sorted(density.items()) if count > 0
        }
        self.congested_cells = [
            {"x": x, "y": y, "count": count}
            for (x, y), count in self.cell_density.items()
            if count >= threshold
        ]
        self.congestion_count = len(self.congested_cells)

    def record_cell_time(self, agent_id: str, cell_type: CellType) -> None:
        agent_times = self.time_spent_by_agent_id.setdefault(
            agent_id, defaultdict(int)
        )
        agent_times[cell_type.value] += 1

    def record_restricted_breach(self, handled: bool = True) -> None:
        self.breach_detected += 1
        if handled:
            self.breach_handled += 1

    def record_boundary_block(self) -> None:
        self.blocked_boundary_attempts += 1

    def record_gate_congestion(self) -> None:
        self.gate_congestion_events += 1

    def record_exit(self) -> None:
        self.exit_events += 1

    def record_penalty_traversal(self) -> None:
        self.penalty_cell_traversals += 1

    def to_dict(self) -> dict:
        return {
            "breach_detected": self.breach_detected,
            "breach_handled": self.breach_handled,
            "blocked_boundary_attempts": self.blocked_boundary_attempts,
            "gate_congestion_events": self.gate_congestion_events,
            "exit_events": self.exit_events,
            "penalty_cell_traversals": self.penalty_cell_traversals,
            "unresolved_breaches": self.unresolved_breaches,
            "cell_density": [
                {"x": x, "y": y, "count": count}
                for (x, y), count in sorted(self.cell_density.items())
            ],
            "congestion_count": self.congestion_count,
            "congested_cells": list(self.congested_cells),
            "time_spent_by_agent_id": {
                agent_id: dict(cell_times)
                for agent_id, cell_times in self.time_spent_by_agent_id.items()
            },
        }
