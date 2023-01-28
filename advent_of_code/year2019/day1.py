"""Solves the puzzle for Day 1 of Advent of Code 2019.

The Tyranny of the Rocket Equation

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/1
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 1
    TITLE = "The Tyranny of the Rocket Equation"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"\d+", int_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum((mass // 3) - 2 for mass in self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        def calc_fuel(mass: int) -> int:
            fuel = (mass // 3) - 2
            return 0 if fuel <= 0 else fuel + calc_fuel(fuel)

        return sum(calc_fuel(mass) for mass in self.input)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
