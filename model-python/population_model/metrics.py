from collections import defaultdict
from dataclasses import dataclass, field

from population_model.terrain import CellType


@dataclass
class TerrainMetrics:
    breach_detected: int = 0
    breach_handled: int = 0
    blocked_boundary_attempts: int = 0
    gate_congestion_events: int = 0
    exit_events: int = 0
    penalty_cell_traversals: int = 0
    time_spent_by_agent_id: dict[str, dict[str, int]] = field(default_factory=dict)

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
            "time_spent_by_agent_id": {
                agent_id: dict(cell_times)
                for agent_id, cell_times in self.time_spent_by_agent_id.items()
            },
        }
