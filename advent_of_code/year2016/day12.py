"""Solves the puzzle for Day 12 of Advent of Code 2016.

Leonardo's Monorail

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/12
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2016.assembunny import load, run


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 12
    TITLE = "Leonardo's Monorail"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.program = load(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return run(self.program)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return run(self.program, c=1)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
