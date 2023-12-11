"""Solves the puzzle for Day 9 of Advent of Code 2023.

Mirage Maintenance

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/9
"""
from enum import Enum, unique
from itertools import pairwise
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Direction(Enum):
    """Left of Right."""

    left = 0
    right = 1


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 9
    TITLE = "Mirage Maintenance"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input, (r"-?\d+", int_processor), delimiter=" "
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self.solve(Direction.right)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self.solve(Direction.left)

    def solve(self, direction: Direction) -> int:
        """Solve the problem.

        Args:
            direction (Direction): the direction

        Returns:
            int: the answer
        """

        def extrapolate(seq: list[int]) -> int:
            if all(n == 0 for n in seq):
                return 0

            diff = [b - a for a, b in pairwise(seq)]
            if direction == Direction.left:
                return seq[0] - extrapolate(diff)
            return seq[-1] + extrapolate(diff)

        return sum(extrapolate(line) for line in self.input)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
