"""Solves the puzzle for Day 25 of Advent of Code 2022.

Full of Hot Air

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/25
"""
from itertools import count
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 25
    TITLE = "Full of Hot Air"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[0-9=-]+", str_processor))

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        return self._to_snafu(sum(self._to_decimal(x) for x in self.input))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Raises:
            NotImplementedError: always!
        """
        raise NotImplementedError("No part two on Christmas Day!!!")

    def _to_decimal(self, snafu: str) -> int:
        """Convert a SNAFU string into a decimal int.

        Args:
            snafu (str): the SNAFU to convert

        Returns:
            int: the result
        """
        return sum(
            -(5**i) if c == "-" else -(5**i) * 2 if c == "=" else (5**i) * int(c)
            for i, c in enumerate(reversed(snafu))
        )

    def _to_snafu(self, decimal: int) -> str:
        """Convert a decimal int into a SNAFU string.

        Args:
            decimal (int): the input decimal

        Returns:
            str: the SNAFU result
        """
        # calculate the length of the result
        length = next(i for i in count() if decimal < (5**i)) - 1

        # find the partial result, before using the - and = digits
        partial: List[int] = []
        for i in range(length, -1, -1):
            x = decimal // (5**i) if decimal >= (5**i) else 0
            decimal -= x * (5**i)
            partial.append(x)

        # encode the partial result using - and =, building the string in reverse
        encoded = []
        carry = 0
        encoder = {
            0: ("0", 0),
            1: ("1", 0),
            2: ("2", 0),
            3: ("=", 1),
            4: ("-", 1),
            5: ("0", 1),
        }
        for digit in reversed(partial):
            digit += carry
            x, carry = encoder[digit]
            encoded.append(x)

        # handle the last carry
        encoded = encoded + (["1"] * carry)

        return "".join(reversed(encoded))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
