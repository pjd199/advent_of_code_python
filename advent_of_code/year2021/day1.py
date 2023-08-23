"""Solves the puzzle for Day 1 of Advent of Code 2021.

Sonar Sweep

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/1
"""
from itertools import pairwise
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 1
    TITLE = "Sonar Sweep"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"\d+", int_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(window_size=1)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(window_size=3)

    def _solve(self, window_size: int) -> int:
        windows = [
            sum(self.input[i : i + window_size])
            for i in range(len(self.input) - window_size + 1)
        ]
        return sum(1 for a, b in pairwise(windows) if b > a)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
