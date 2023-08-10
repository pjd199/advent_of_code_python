"""A package for co-ordinate Points."""
from dataclasses import dataclass
from enum import Enum, unique


@unique
class Direction(Enum):
    """Superclass for Direction."""

    ...


@unique
class ArrowDirection(Direction):
    """A direction in a move."""

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


@unique
class LetterDirection(Direction):
    """A direction in a move."""

    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


@unique
class CompassDirection(Direction):
    """A direction in a move."""

    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Move:
    """A move with direction and distance."""

    direction: Direction
    distance: int


@dataclass(eq=True)
class Point:
    """A two dimensional point."""

    x: int
    y: int

    def move(self, x: int, y: int) -> None:
        """Return a new Point, shifted by the given offsets.

        Args:
            x (int): the x shift
            y (int): the y shift
        """
        self.x += x
        self.y += y

    def freeze(self) -> "FrozenPoint":
        """Create a FrozenPoint based on this Point.

        Returns:
            FrozenPoint: A FrozenPoint with the same (x,y)
        """
        return FrozenPoint(self.x, self.y)


@dataclass(eq=True, frozen=True)
class FrozenPoint:
    """A two dimensional point - frozen for hashing."""

    x: int
    y: int
