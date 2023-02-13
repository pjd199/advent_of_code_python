"""Solves the puzzle for Day 9 of Advent of Code 2019.

Sensor Boost

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/9
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.IntcodeComputer import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 9
    TITLE = "Sensor Boost"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.computer = IntcodeComputer(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.computer.reset()
        self.computer.append_input(1)
        self.computer.execute()

        return self.computer.read_output()

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self.computer.reset()
        self.computer.append_input(2)
        self.computer.execute()
        return self.computer.read_output()


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
