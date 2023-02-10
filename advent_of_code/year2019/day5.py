"""Solves the puzzle for Day 5 of Advent of Code 2019.

Sunny with a Chance of Asteroids

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/5
"""
from copy import deepcopy
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import execute_intcode, parse_intcode


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 5
    TITLE = "Sunny with a Chance of Asteroids"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_intcode(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return execute_intcode(deepcopy(self.input), [1])[-1]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return execute_intcode(deepcopy(self.input), [5])[-1]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
