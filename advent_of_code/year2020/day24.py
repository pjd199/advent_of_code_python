"""Solves the puzzle for Day 24 of Advent of Code 2020.

Lobby Layout

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/24
"""
from collections import Counter
from collections.abc import Callable
from enum import Enum, unique
from pathlib import Path
from re import findall
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import enum_re, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class _Direction(Enum):
    E = "e"
    SE = "se"
    SW = "sw"
    W = "w"
    NW = "nw"
    NE = "ne"


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 24
    TITLE = "Lobby Layout"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                r"[nesw]+",
                lambda m: [
                    _Direction(x) for x in findall(rf"({enum_re(_Direction)})", m[0])
                ],
            ),
        )

        # move using the "double co-ordinate" or interlaced system
        self.move: dict[_Direction, Callable[[int, int], tuple[int, int]]] = {
            _Direction.E: lambda x, y: (x + 2, y),
            _Direction.SE: lambda x, y: (x + 1, y + 1),
            _Direction.SW: lambda x, y: (x - 1, y + 1),
            _Direction.W: lambda x, y: (x - 2, y),
            _Direction.NW: lambda x, y: (x - 1, y - 1),
            _Direction.NE: lambda x, y: (x + 1, y - 1),
        }
        self.black_tiles: set[tuple[int, int]] = set()

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._lay_floor()
        return len(self.black_tiles)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._lay_floor()
        black_tiles = set(self.black_tiles)
        for _ in range(100):
            neighbours = Counter(
                self.move[direction](x, y)
                for (x, y) in black_tiles
                for direction in _Direction
            )
            black_tiles = {
                (x, y)
                for (x, y), count in neighbours.items()
                if count == 2 or (count == 1 and (x, y) in black_tiles)
            }

        return len(black_tiles)

    def _lay_floor(self) -> None:
        """Lay the floor."""
        if not self.black_tiles:
            self.black_tiles = set()
            for tile in self.input:
                x, y = 0, 0
                for direction in tile:
                    x, y = self.move[direction](x, y)
                if (x, y) in self.black_tiles:
                    self.black_tiles.remove((x, y))
                else:
                    self.black_tiles.add((x, y))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
