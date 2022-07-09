"""Solution for day 25 of Advent of Code 2015."""
from re import match
from typing import List

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver the puzzle."""

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the solver.

        Args:
            puzzle_input (List[str]): the puzzle input

        Raises:
            RuntimeError: raised in unable to parse input
        """
        # validate and parse the input
        if puzzle_input is None or len(puzzle_input) == 0:
            raise RuntimeError("Puzzle input is empty")

        # parse the input into integers
        m = match(
            r"^To continue, please consult the code grid in the manual.  "
            r"Enter the code at row (?P<row>[0-9]+), "
            r"column (?P<col>[0-9]+).$",
            puzzle_input[0],
        )

        if m:
            self.row = int(m.groupdict()["row"])
            self.col = int(m.groupdict()["col"])
        else:
            raise RuntimeError("Invalid input at line 1")

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

    def solve_all(self) -> List[int]:
        """Solve the one and only part to this puzzle.

        Returns:
            List[int]: the result
        """
        return [self.solve_part_one()]
