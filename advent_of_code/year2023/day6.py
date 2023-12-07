"""Solves the puzzle for Day 6 of Advent of Code 2023.

Wait For It

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/6
"""
from math import prod, sqrt
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    str_processor_group,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 6
    TITLE = "Wait For It"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.times, self.distances = parse_lines(
            puzzle_input, (r"(?:Time|Distance): +([\d ]+)", str_processor_group(1))
        )

    def curve_width(self, time: int, distance: int) -> int:
        """Find the width of the curve at the x axis crossing.

        Args:
            time (int): the time
            distance (int): the distance

        Returns:
            int: the result
        """
        a = -1
        b = time
        c = -distance
        return abs(
            int(-(b / (2 * a)) + sqrt((b / (2 * a)) ** 2 - (c / a)))
            - int(-(b / (2 * a)) - sqrt((b / (2 * a)) ** 2 - (c / a)))
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return prod(
            self.curve_width(int(time), int(distance))
            for time, distance in zip(self.times.split(), self.distances.split())
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        time = int(self.times.replace(" ", ""))
        distance = int(self.distances.replace(" ", ""))
        return self.curve_width(time, distance)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
