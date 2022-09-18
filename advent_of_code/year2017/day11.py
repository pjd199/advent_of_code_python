"""Solves the puzzle for Day 11 of Advent of Code 2017.

Hex Ed

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/11
"""
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Callable, Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import enum_processor, enum_re, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class _Direction(Enum):
    N = "n"
    NE = "ne"
    SE = "se"
    S = "s"
    SW = "sw"
    NW = "nw"


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 11
    TITLE = "Hex Ed"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input,
            rf"({enum_re(_Direction)})",
            enum_processor(_Direction),
            delimiter=",",
        )[0]
        self.max_distance = -1
        self.final_distance = -1

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if self.final_distance == -1:
            self._solve()
        return self.final_distance

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if self.max_distance == -1:
            self._solve()
        return self.max_distance

    def _solve(self) -> None:
        # move using the "double co-ordinate" or interlaced system
        move: Dict[_Direction, Callable[[int, int], Tuple[int, int]]] = {
            _Direction.N: lambda x, y: (x, y - 2),
            _Direction.NE: lambda x, y: (x + 1, y - 1),
            _Direction.SE: lambda x, y: (x + 1, y + 1),
            _Direction.S: lambda x, y: (x, y + 2),
            _Direction.SW: lambda x, y: (x - 1, y + 1),
            _Direction.NW: lambda x, y: (x - 1, y - 1),
        }

        x, y = 0, 0
        self.max_distance = 0
        for direction in self.input:
            x, y = move[direction](x, y)
            self.max_distance = max(self.max_distance, (abs(x) + abs(y)) // 2)

        self.final_distance = (abs(x) + abs(y)) // 2


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
