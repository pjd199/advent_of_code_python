"""Solves the puzzle for Day 2 of Advent of Code 2021.

Dive!

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/2
"""
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, enum_re, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class _Direction(Enum):
    forward = "forward"
    down = "down"
    up = "up"


@dataclass
class _Command:
    direction: _Direction
    value: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 2
    TITLE = "Dive!"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                rf"(?P<direction>{enum_re(_Direction)}) (?P<value>\d+)",
                dataclass_processor(_Command),
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        x, y = 0, 0
        moves: dict[_Direction, Callable[[int], tuple[int, int]]] = {
            _Direction.forward: lambda v: (x + v, y),
            _Direction.down: lambda v: (x, y + v),
            _Direction.up: lambda v: (x, y - v),
        }
        for command in self.input:
            x, y = moves[command.direction](command.value)
        return abs(x) * abs(y)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        x, y = 0, 0
        aim = 0
        moves: dict[_Direction, Callable[[int], tuple[int, int, int]]] = {
            _Direction.forward: lambda v: (x + v, y + (aim * v), aim),
            _Direction.down: lambda v: (x, y, aim + v),
            _Direction.up: lambda v: (x, y, aim - v),
        }
        for command in self.input:
            x, y, aim = moves[command.direction](command.value)
        return abs(x) * abs(y)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
