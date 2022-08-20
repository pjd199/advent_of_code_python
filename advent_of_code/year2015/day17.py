"""Solves the puzzle for Day 17 of Advent of Code 2015.

No Such Thing as Too Much

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/17
"""
from itertools import combinations, groupby
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 17
    TITLE = "No Such Thing as Too Much"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if puzzle_input is None or len(puzzle_input) == 0:
            raise RuntimeError("Puzzle input is empty")

        pattern = compile(r"(?P<size>[0-9]+)")
        self.sizes = []
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                self.sizes.append(int(match["size"]))
            else:
                raise RuntimeError(f"Parse error on line {i + 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return len(
            [
                c
                for r in range(len(self.sizes))
                for c in combinations(self.sizes, r)
                if sum(c) == 150
            ]
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        return [
            (k, len(list(g)))
            for k, g in groupby(
                [
                    r
                    for r in range(len(self.sizes))
                    for c in combinations(self.sizes, r)
                    if sum(c) == 150
                ]
            )
        ][0][1]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
