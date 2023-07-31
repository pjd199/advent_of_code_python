"""Solves the puzzle for Day 25 of Advent of Code 2015.

Let It Snow

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/25
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver the puzzle."""

    YEAR = 2015
    DAY = 25
    TITLE = "Let It Snow"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the solver.

        Args:
            puzzle_input (List[str]): the puzzle input
        """
        self.row, self.col = parse_single_line(
            puzzle_input,
            r"To continue, please consult the code grid in the manual.  "
            r"Enter the code at row (?P<row>[0-9]+), "
            r"column (?P<col>[0-9]+).",
            int_tuple_processor,
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # translate row, column in seqeuence number
        # find the position in the sequence of row, col, based on the
        # formula for triangular numbers - (n * (n - 1)) / 2

        # this was the loop based approach I derived,
        # but mathmatical approach below is much cleaner!!!
        seq = (
            1
            + (((self.row - 1) * self.row) // 2)
            + (((self.col + self.row - 1) * (self.col + self.row)) // 2)
            - ((self.row * (self.row + 1)) // 2)
        )

        # iterate to find the nth number in the sequence
        code = 20151125
        for _ in range(seq - 1):
            code = (code * 252533) % 33554393

        # find the answers and return
        return code

    def solve_part_two(self) -> int:
        """There is no part two on Christmas Day.

        Raises:
            NotImplementedError: Always.
        """
        raise NotImplementedError("No part two on Christmas Day!!!")


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
