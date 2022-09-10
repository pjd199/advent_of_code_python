"""Solves the puzzle for Day 6 of Advent of Code 2016.

Signals and Noise

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from collections import defaultdict
from pathlib import Path
from sys import path
from typing import DefaultDict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 6
    TITLE = "Signals and Noise"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"(?P<message>[a-z]+)", str_processor))

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


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
