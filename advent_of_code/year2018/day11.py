"""Solves the puzzle for Day 11 of Advent of Code 2018.

Chronal Charge

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/11
"""
from pathlib import Path
from sys import path

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 11
    TITLE = "Chronal Charge"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"\d+", int_processor)
        self.ready = False

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        if not self.ready:
            self._calc_power_levels()

        _, largest_x, largest_y, _ = self._find_largest(3)

        return f"{largest_x},{largest_y}"

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        if not self.ready:
            self._calc_power_levels()

        _, largest_x, largest_y, largest_size = max(
            self._find_largest(i) for i in range(1, 300)
        )

        return f"{largest_x},{largest_y},{largest_size}"

    def _calc_power_levels(self) -> None:
        """Calculate the power levels."""
        self.grid = np.array(
            [
                [
                    int(f"{((((x + 10) * y) + self.input) * (x + 10)):03}"[-3]) - 5
                    for x in range(1, 301)
                ]
                for y in range(1, 301)
            ]
        )
        self.ready = True

    def _find_largest(self, size: int) -> tuple[int, int, int, int]:
        """Find the largest power for the given sized square.

        Args:
            size (int): the size of the square

        Returns:
            tuple[int, int, int, int]: a tuple of (power, x, y, size)
        """
        largest, largest_x, largest_y = max(
            [
                (
                    np.sum(self.grid[y : (y + size), x : (x + size)]),
                    x + 1,
                    y + 1,
                )
                for y in range(0, 300 - (size - 1))
                for x in range(0, 300 - (size - 1))
            ]
        )

        return largest, largest_x, largest_y, size


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
