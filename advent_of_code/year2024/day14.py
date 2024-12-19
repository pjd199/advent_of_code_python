"""Solves the puzzle for Day 14 of Advent of Code 2024.

Restroom Redoubt

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/14
"""

from collections.abc import Sequence
from math import prod
from statistics import stdev

from advent_of_code.utils.parser import int_sequence_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 14
    TITLE = "Restroom Redoubt"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", int_sequence_processor)
        )
        self.width = 101
        self.height = 103

    def _robots(self, seconds: int) -> Sequence[tuple[int, int]]:
        return [
            ((px + (seconds * vx)) % self.width, (py + (seconds * vy)) % self.height)
            for px, py, vx, vy in self.input
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        robots = self._robots(100)

        quadrants = [
            (0, 0, self.width // 2, self.height // 2),
            (self.width // 2 + 1, 0, self.width, self.height // 2),
            (0, self.height // 2 + 1, self.width // 2, self.height),
            (self.width // 2 + 1, self.height // 2 + 1, self.width, self.height),
        ]

        return prod(
            sum(1 for x, y in robots if x1 <= x < x2 and y1 <= y < y2)
            for x1, y1, x2, y2 in quadrants
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        x_offset, y_offset = (
            a.index(min(a))
            for a in zip(
                *(
                    (stdev(coord) for coord in zip(*self._robots(seconds)))
                    for seconds in range(max(self.height, self.width))
                )
            )
        )
        return min(
            {x_offset + i * self.width for i in range(self.height)}
            & {y_offset + i * self.height for i in range(self.width)}
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
