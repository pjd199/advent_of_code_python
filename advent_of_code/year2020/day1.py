"""Solves the puzzle for Day 1 of Advent of Code 2020.

Report Repair

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/1
"""
from itertools import combinations
from math import prod
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 1
    TITLE = "Report Repair"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r".*", int_processor))

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
        return self._solve(3)

    def _solve(self, size: int) -> int:
        """Solve the puzzle.

        Args:
            size (int): the window size

        Returns:
            int: the result
        """
        return next(prod(c) for c in combinations(self.input, size) if sum(c) == 2020)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
