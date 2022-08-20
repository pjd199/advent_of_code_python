"""Solves the puzzle for Day 19 of Advent of Code 2016.

An Elephant Named Joseph

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/19
"""
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 19
    TITLE = "An Elephant Named Joseph"

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

        # parse the input
        pattern = compile(r"\d+")
        for i, line in enumerate(puzzle_input):
            if (m := pattern.fullmatch(line)) and (i == 0):
                self.number_of_elves = int(m[0])
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i + 1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

            running mathmatical solution for "Josephus problem"
            https://en.wikipedia.org/wiki/Josephus_problem

        Returns:
            int: the answer
        """
        exponent = 1
        while (2 ** int(exponent + 1)) <= self.number_of_elves:
            exponent += 1
        return 2 * (self.number_of_elves - int(2**exponent)) + 1

    def solve_part_two(self) -> int:  # pragma: no cover
        """Solve part two of the puzzle.

            Following the mathmatical solution to part one,
            this formula was developed by observing the pattern
            for first 100 numbers

        Returns:
            int: the answer
        """
        exponent = 1
        while (3 ** int(exponent + 1)) <= self.number_of_elves:
            exponent += 1

        if self.number_of_elves < 3:
            return 1
        else:
            if self.number_of_elves > (2 * int(3**exponent)):
                return (2 * self.number_of_elves) - int(3 ** (exponent + 1))
            else:
                return self.number_of_elves - int(3**exponent)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
