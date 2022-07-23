"""Solves the puzzle for Day 9 of Advent of Code 2016."""
from re import compile
from typing import List

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
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
            or len(puzzle_input) != 1
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        pattern = compile(r"([A-Z]|\(\d+x\d+\))+")
        if pattern.fullmatch(puzzle_input[0]):
            self.input = puzzle_input[0]
        else:
            raise RuntimeError(f"Unable to parse {puzzle_input[0]} on line 1")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._decompressed_length(self.input, 1)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._decompressed_length(self.input, 2)

    def _decompressed_length(self, data: str, version: int) -> int:
        """Calculate the decompressed length, depending on the version.

            Version 1 - no recursion
            Version 2 - recursion

        Args:
            data (str): the input string
            version (int): the version code

        Returns:
            int: the length of the decompressed string.
        """
        length = 0
        i = 0
        pattern = compile(r"\((?P<len>\d+)x(?P<repeat>\d+)\)")
        while i < len(data):
            if m := pattern.match(data[i:]):
                if version == 1:
                    length += int(m["len"]) * int(m["repeat"])
                else:
                    length += self._decompressed_length(
                        data[i + len(m[0]) : i + len(m[0]) + int(m["len"])], version
                    ) * int(m["repeat"])
                i += len(m[0]) + int(m["len"])
            else:
                length += 1
                i += 1

        return length
