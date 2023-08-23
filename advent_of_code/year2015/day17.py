"""Solves the puzzle for Day 17 of Advent of Code 2015.

No Such Thing as Too Much

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/17
"""
from itertools import combinations, groupby
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 17
    TITLE = "No Such Thing as Too Much"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.sizes = parse_lines(puzzle_input, (r"[0-9]+", int_processor))

    @cache_result
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

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        return next(
            (k, len(list(g)))
            for k, g in groupby(
                [
                    r
                    for r in range(len(self.sizes))
                    for c in combinations(self.sizes, r)
                    if sum(c) == 150
                ]
            )
        )[1]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
