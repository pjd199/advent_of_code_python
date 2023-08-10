"""Solves the puzzle for Day 13 of Advent of Code 2022.

Distress Signal

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/13
"""
from functools import cmp_to_key
from itertools import chain
from json import loads
from math import prod
from pathlib import Path
from sys import path
from typing import Any, List, Union

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, split_sections
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 13
    TITLE = "Distress Signal"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = [
            parse_lines(section, (r"[\[0-9,\]]+", lambda m: loads(m[0])))
            for section in split_sections(puzzle_input)
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            i + 1
            for i, (left, right) in enumerate(self.input)
            if self._compare(left, right) <= 0
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        dividers = [[[2]], [[6]]]
        packets = sorted(
            list(chain.from_iterable(self.input)) + dividers,
            key=cmp_to_key(self._compare),
        )

        return prod(i + 1 for i, x in enumerate(packets) if x in dividers)

    def _compare(
        self, left: Union[int, List[Any]], right: Union[int, List[Any]]
    ) -> int:
        result = -1
        if isinstance(left, int) and isinstance(right, int):
            result = left - right
        elif isinstance(left, int) and isinstance(right, list):
            result = self._compare([left], right)
        elif isinstance(left, list) and isinstance(right, int):
            result = self._compare(left, [right])
        elif isinstance(left, list) and isinstance(right, list):
            # left and right are lists
            result = len(left) - len(right)
            for i in range(min(len(left), len(right))):
                res = self._compare(left[i], right[i])
                if res != 0:
                    result = res
                    break
            return result

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
