"""Solves the puzzle for Day 4 of Advent of Code 2015.

The Ideal Stocking Stuffer

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/4
"""
from hashlib import md5
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
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
        """
        self.secret = parse_single_line(puzzle_input, r"[a-z]+", str_processor)

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
