"""Solves the puzzle for Day 1 of Advent of Code 2015.

Not Quite Lisp

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/1
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2015
    DAY = 1
    TITLE = "Not Quite Lisp"

    """Solves the puzzle."""

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        if not all([c == "(" or c == ")" for c in puzzle_input[0]]):
            raise RuntimeError(
                f"Puzzle input should only contain '(' or ')', "
                f"found {puzzle_input[0]}"
            )

        # translate the input into +1 and -1 floor movements
        self.input = [1 if x == "(" else -1 for x in puzzle_input[0]]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # find the final score by moving up 1 floor for a '(',
        # and down one floor for a ')'
        return sum(self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        floor = 0
        for i, x in enumerate(self.input):
            floor += x
            if floor < 0:
                floor = i + 1
                break

        return floor


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
