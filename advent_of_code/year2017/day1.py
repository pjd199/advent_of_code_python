"""Solves the puzzle for Day 1 of Advent of Code 2017.

Inverse Captcha

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/1
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 1
    TITLE = "Inverse Captcha"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"\d", int_processor), delimiter=""
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(1)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(len(self.input) // 2)

    def _solve(self, start: int) -> int:
        """Solve the puzzle.

        Args:
            start (int): starting position

        Returns:
            int: result
        """
        return sum(
            x
            for x, y in zip(self.input, self.input[start:] + self.input[:start])
            if x == y
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
