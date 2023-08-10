"""Solves the puzzle for Day 25 of Advent of Code 2020.

Combo Breaker

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/25
"""
from pathlib import Path
from sys import path
from typing import Generator, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 25
    TITLE = "Combo Breaker"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"\d+", int_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """

        def transform(subject_number: int) -> Generator[int, None, None]:
            value = subject_number
            while True:
                value *= subject_number
                value %= 20201227
                yield value

        loop_size, value = next(
            (i + 1, v) for i, v in enumerate(transform(7)) if v in self.input
        )
        key = next(k for k in self.input if k != value)
        return next((v for i, v in enumerate(transform(key)) if i >= loop_size - 1))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: but never does!

        Raises:
            NotImplementedError: always!
        """
        raise NotImplementedError("No part two on Christmas Day!!!")


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
