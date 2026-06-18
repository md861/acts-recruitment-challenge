## @file state.py
#  @brief Shared domain state types for the population model.
#
#  Defines serializable position, heading, and agent records used across model
#  modules and public snapshots.

from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y}


@dataclass
class Heading:
    dx: int
    dy: int

    def to_dict(self) -> dict:
        return {"dx": self.dx, "dy": self.dy}


@dataclass
class Agent:
    id: str
    role: str
    status: str
    position: Position
    heading: Heading

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "role": self.role,
            "status": self.status,
            "position": self.position.to_dict(),
            "heading": self.heading.to_dict(),
        }
