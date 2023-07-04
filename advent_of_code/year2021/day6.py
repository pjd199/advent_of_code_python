"""Solves the puzzle for Day 6 of Advent of Code 2021.

Lanternfish

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/6
"""
from pathlib import Path
from sys import path
from typing import List

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 6
    TITLE = "Lanternfish"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"\d+", int_processor), delimiter=","
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(80)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(256)

    def _solve(self, days: int) -> int:
        """Solve the puzzle.

        Args:
            days (int): number of days to simulate

        Returns:
            int: total number of fish on the last day
        """
        fish = np.bincount(self.input, minlength=9)
        for _ in range(days):
            fish = np.roll(fish, shift=-1)
            fish[6] += fish[8]
        return int(np.sum(fish))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
