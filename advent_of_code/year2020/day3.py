"""Solves the puzzle for Day 3 of Advent of Code 2020.

Toboggan Trajectory

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/3
"""
from itertools import count
from math import prod
from pathlib import Path
from sys import path
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 3
    TITLE = "Toboggan Trajectory"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"[#.]", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve([(3, 1)])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve([(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])

    def _solve(self, slopes: List[Tuple[int, int]]) -> int:
        """Solve the puzzle.

        Args:
            slopes (List[Tuple[int, int]]): the slopes to descend

        Returns:
            int: the result
        """
        return prod(
            sum(
                1
                for x, y in zip(count(0, right), range(0, len(self.input), down))
                if self.input[y][x % len(self.input[y])] == "#"
            )
            for right, down in slopes
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
