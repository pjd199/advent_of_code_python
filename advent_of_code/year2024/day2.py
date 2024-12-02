"""Solves the puzzle for Day 2 of Advent of Code 2024.

Red-Nosed Reports

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/2
"""

from itertools import pairwise
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 2
    TITLE = "Red-Nosed Reports"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"\d+", int_processor), delimiter=r" ")

    def safe(self, reports: list[int]) -> bool:
        """Check if a report is safe.

        Args:
            reports (list[int]): the reports

        Returns:
            bool: True if safe, otherwise false
        """
        return all(-3 <= x - y <= -1 for x, y in pairwise(reports)) or all(
            1 <= x - y <= 3 for x, y in pairwise(reports)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(1 for line in self.input if self.safe(line))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1
            for line in self.input
            if self.safe(line)
            or any(self.safe(line[:i] + line[i + 1 :]) for i in range(len(line)))
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
