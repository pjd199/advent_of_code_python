"""Solves the puzzle for Day 1 of Advent of Code 2015.

Not Quite Lisp

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/1
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2015
    DAY = 1
    TITLE = "Not Quite Lisp"

    """Solves the puzzle."""

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input,
            (r"[\(\)]", lambda m: 1 if m[0] == "(" else -1),
        )

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self.input)

    @cache_result
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
