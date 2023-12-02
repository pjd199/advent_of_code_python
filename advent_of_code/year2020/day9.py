"""Solves the puzzle for Day 9 of Advent of Code 2020.

Encoding Error

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/9
"""
from itertools import combinations, takewhile
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 9
    TITLE = "Encoding Error"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"\d+", int_processor))
        self.window = 25
        self.invalid = -1

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._find_invalid()
        return self.invalid

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._find_invalid()

        # break the input into chunks of contiguus values less than
        # the invalid numbers
        num_iter = iter(self.input)
        chunks = []
        while chunk := list(takewhile(lambda x: x < self.invalid, num_iter)):
            chunks.append(chunk)

        # find the first window where all the numbers add up to the invalid number
        window = next(
            window
            for window in (
                next(
                    (
                        self.input[i : i + size]
                        for i in range(len(chunk) - size)
                        if sum(chunk[i : i + size]) == self.invalid
                    ),
                    None,
                )
                for chunk in chunks
                for size in range(2, len(chunk))
            )
            if window
        )

        # return the desired result
        return min(window) + max(window)

    def _find_invalid(self) -> None:
        """Find the first invalid code, but only once."""
        if self.invalid == -1:
            self.invalid = next(
                self.input[i]
                for i in range(self.window, len(self.input))
                if self.input[i]
                not in {
                    a + b for a, b in combinations(self.input[i - self.window : i], 2)
                }
            )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
