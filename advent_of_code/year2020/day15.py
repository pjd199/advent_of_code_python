"""Solves the puzzle for Day 15 of Advent of Code 2020.

Rambunctious Recitation

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/15
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 15
    TITLE = "Rambunctious Recitation"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"\d+", int_processor), delimiter=","
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(2020)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(30000000)

    def _solve(self, steps: int) -> int:
        mem = {x: i + 1 for i, x in enumerate(self.input)}
        last = self.input[-1]
        for i in range(len(self.input), steps):
            mem[last], last = (i, i - mem.get(last, i))
        return last


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
