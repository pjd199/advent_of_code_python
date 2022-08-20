"""Solves the puzzle for Day 4 of Advent of Code 2015.

The Ideal Stocking Stuffer

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/4
"""
from hashlib import md5
from pathlib import Path
from string import ascii_lowercase
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 4
    TITLE = "The Ideal Stocking Stuffer"

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

        if len(puzzle_input) == 1 and all(
            x in ascii_lowercase for x in puzzle_input[0]
        ):
            self.secret = puzzle_input[0]
        else:
            raise RuntimeError(f"Unable to parse input: {puzzle_input[0]}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._find(self.secret, "00000")

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        return self._find(self.secret, "000000")

    def _find(self, secret: str, prefix: str) -> int:
        """Find the solution.

            Find the MD5 hash of the secret + an integer, where the
            start result starts with the given prefix.

        Args:
            secret (str): the secret input
            prefix (str): the prefix to search for

        Returns:
            int: the integer that gives the requested prefix
        """
        i = 0
        while True:
            if (
                # python 3.9 introduced usedforsecurity=False for MD5 function,
                # which raises a security issue for bandit - # nosec is used
                # to ignore this, as there are no security issues here
                md5((secret + str(i)).encode())  # nosec
                .hexdigest()
                .startswith(prefix)
            ):
                break
            i += 1
        return i


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
