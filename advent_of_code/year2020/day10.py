"""Solves the puzzle for Day 10 of Advent of Code 2020.

Adapter Array

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/10
"""
from collections import Counter
from functools import lru_cache
from itertools import pairwise
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 10
    TITLE = "Adapter Array"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"\d+", int_processor))
        self.adapters: set[int] = set()

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.prepare()
        ordered = sorted(self.adapters)
        differences = Counter(b - a for a, b in pairwise(ordered))
        return differences[1] * differences[3]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self.prepare()

        @lru_cache(maxsize=len(self.input))
        def possibilities(item: int) -> int:
            if item == 0:
                return 1
            return sum(
                possibilities(x)
                for x in (a for a in range(item - 3, item) if a in self.adapters)
            )

        return possibilities(max(self.adapters))

    def prepare(self) -> None:
        """Prepare the adapters."""
        if not self.adapters:
            self.adapters = set(self.input)
            self.adapters |= {0, max(self.adapters) + 3}


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
