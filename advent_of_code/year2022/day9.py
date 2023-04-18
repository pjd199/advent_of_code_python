"""Solves the puzzle for Day 9 of Advent of Code 2022.

Rope Bridge

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/9
"""
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Callable, Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, enum_re, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Direction(Enum):
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


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 9
    TITLE = "Rope Bridge"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                rf"(?P<direction>{enum_re(Direction)}) (?P<distance>\d+)",
                dataclass_processor(Move),
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(2)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(10)

    def _solve(self, rope_length: int) -> int:
        """Solve the puzzle.

        Args:
            rope_length (int): the length of the rope to simulate

        Returns:
            int: the number of unique places the end of the rope has visited
        """
        ropes = [Point(0, 0) for _ in range(rope_length)]
        visited = {ropes[-1].freeze()}

        # movements for the head of the rope
        moves: Dict[Direction, Callable[[Point], None]] = {
            Direction.UP: lambda p: p.move(0, -1),
            Direction.DOWN: lambda p: p.move(0, 1),
            Direction.LEFT: lambda p: p.move(-1, 0),
            Direction.RIGHT: lambda p: p.move(1, 0),
        }

        # movement as the rope pulls along each knot in the rope
        pull: Dict[Tuple[int, int], Callable[[Point], None]] = {
            (-1, -2): lambda p: p.move(-1, -1),
            (0, -2): lambda p: p.move(0, -1),
            (1, -2): lambda p: p.move(1, -1),
            (-2, -2): lambda p: p.move(-1, -1),
            (-2, -1): lambda p: p.move(-1, -1),
            (-2, 0): lambda p: p.move(-1, 0),
            (-2, 1): lambda p: p.move(-1, 1),
            (-2, 2): lambda p: p.move(-1, 1),
            (2, -2): lambda p: p.move(1, -1),
            (2, -1): lambda p: p.move(1, -1),
            (2, 0): lambda p: p.move(1, 0),
            (2, 1): lambda p: p.move(1, 1),
            (2, 2): lambda p: p.move(1, 1),
            (-1, 2): lambda p: p.move(-1, 1),
            (0, 2): lambda p: p.move(0, 1),
            (1, 2): lambda p: p.move(1, 1),
            (-1, -1): lambda p: None,
            (0, -1): lambda p: None,
            (1, -1): lambda p: None,
            (-1, 0): lambda p: None,
            (0, 0): lambda p: None,
            (1, 0): lambda p: None,
            (-1, 1): lambda p: None,
            (0, 1): lambda p: None,
            (1, 1): lambda p: None,
        }

        for move in self.input:
            for _ in range(move.distance):
                # move the head of the rope
                moves[move.direction](ropes[0])
                # move each knot in the rope, working head to tail
                for i in range(1, len(ropes)):
                    pull[
                        (
                            ropes[i - 1].x - ropes[i].x,
                            ropes[i - 1].y - ropes[i].y,
                        )
                    ](ropes[i])
                # add the last knot to the visited set
                visited.add(ropes[-1].freeze())

        return len(visited)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
