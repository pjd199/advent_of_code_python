"""Solves the puzzle for Day 17 of Advent of Code 2017.

Spinlock

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/17
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 17
    TITLE = "Spinlock"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"\d+", int_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        buffer = [0]
        position = 0

        for i in range(1, 2018):
            position = (position + self.input) % len(buffer) + 1
            buffer.insert(position, i)

        return buffer[position + 1]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        position = 0
        step = self.input

        result = 0
        for i in range(1, 50000000):
            position = (position + step) % i + 1
            if position == 1:
                result = i

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
