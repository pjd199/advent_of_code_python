"""Solves the puzzle for Day 16 of Advent of Code 2016.

# Dragon Checksum

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/16
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
    DAY = 16
    TITLE = "Dragon Checksum"

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
        pattern = compile(r"[01]+")
        for i, line in enumerate(puzzle_input):
            if (m := pattern.fullmatch(line)) and (i == 0):
                self.input = m[0]
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        return self._checksum(272)

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        return self._checksum(35651584)

    def _checksum(self, length: int) -> str:
        # pad data to the correct length
        data = self.input
        while len(data) < length:
            data = "".join(
                [data, "0", "".join("1" if x == "0" else "0" for x in reversed(data))]
            )
        data = data[:length]

        # calculate the checksum
        checksum = list(data)
        while len(checksum) % 2 == 0:
            checksum = [
                "1" if x == y else "0" for x, y in zip(checksum[::2], checksum[1::2])
            ]

        # done
        return "".join(checksum)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
