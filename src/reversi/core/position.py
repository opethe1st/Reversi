from dataclasses import dataclass
from reversi.utils import Enum


@dataclass(unsafe_hash=True)
class Position:
    x: int
    y: int


@dataclass(unsafe_hash=True)
class Direction:
    dx: int = 0
    dy: int = 0

    def __add__(self, other):
        return Direction(dx=self.dx+other.dx, dy=self.dy+other.dy)


class CardinalDirection(Enum):
    NORTH = Direction(dy=-1)
    WEST = Direction(dx=1)
    EAST = Direction(dx=-1)
    SOUTH = Direction(dy=1)
    NORTH_WEST = NORTH + WEST
    NORTH_EAST = NORTH + EAST
    SOUTH_EAST = SOUTH + EAST
    SOUTH_WEST = SOUTH + WEST
