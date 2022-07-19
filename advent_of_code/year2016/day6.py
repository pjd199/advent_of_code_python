"""Solves the puzzle for Day 6 of Advent of Code 2016."""
from collections import defaultdict
from re import compile
from typing import DefaultDict, List

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
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        self.input = []
        pattern = compile(r"(?P<message>[a-z]+)")
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.input.append(m["message"])
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i}")

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        return self._decode(find_most_common=True)

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        return self._decode(find_most_common=False)

    def _decode(self, find_most_common: bool) -> str:
        """Decode the message.

        Args:
            find_most_common (bool): if True, find the most common characters

        Returns:
            str: the decoded message
        """
        # count the occurances
        counters: DefaultDict[int, DefaultDict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        for line in self.input:
            for i, c in enumerate(line):
                counters[i][c] += 1

        # find the most frequent
        message = [""] * len(counters)
        for i, counter in counters.items():
            frequencies = sorted(
                counter.items(), key=lambda x: x[1], reverse=find_most_common
            )
            if frequencies:
                message[i] = frequencies[0][0]

        return "".join(message)
