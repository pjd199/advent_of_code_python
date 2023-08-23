"""Solves the puzzle for Day 8 of Advent of Code 2022.

Treetop Tree House

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/8
"""
from itertools import takewhile
from math import prod
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 8
    TITLE = "Treetop Tree House"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"\d", int_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return (
            sum(
                1
                for y in range(1, len(self.input) - 1)
                for x in range(1, len(self.input[y]) - 1)
                if any(max(view) < self.input[y][x] for view in self.views(x, y))
            )
            + 2 * (len(self.input) + len(self.input[0]))
            - 4
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        def view_length(view: list[int], height: int) -> int:
            count = len(list(takewhile(lambda a: a < height, view)))
            return count + (1 if count < len(view) else 0)

        return max(
            prod(view_length(view, self.input[y][x]) for view in self.views(x, y))
            for y in range(len(self.input))
            for x in range(len(self.input[y]))
        )

    def views(self, x: int, y: int) -> list[list[int]]:
        """Return all the trees in each direction [up, down, left, right].

        Args:
            x (int): the starting x coordinate
            y (int): the starting y coordinate

        Returns:
            list[list[int]]: the result
        """
        return [
            [self.input[y1][x] for y1 in range(y - 1, -1, -1)],  # up
            [self.input[y1][x] for y1 in range(y + 1, len(self.input))],  # down
            [self.input[y][x1] for x1 in range(x - 1, -1, -1)],  # left
            [self.input[y][x1] for x1 in range(x + 1, len(self.input[y]))],  # right
        ]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
