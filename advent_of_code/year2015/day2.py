"""Solves the puzzle for Day 2 of Advent of Code 2015.

I Was Told There Would Be No Math

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/2
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 2
    TITLE = "I Was Told There Would Be No Math"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"([0-9]+)x([0-9]+)x([0-9]+)", int_tuple_processor)
        )

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # cacluate the ammount of wrapping paper, as the sum of the
        # total area of the six sides of each cuboid,
        # plus the area of the smallest side of each cuboid
        # (dimensions are sorted during parsing in __init__)
        return sum(
            (3 * a * b) + (2 * b * c) + (2 * c * a)
            for a, b, c in (sorted(x) for x in self.input)
        )

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # calculate the ammount of ribbon, as the sum of the perimiter
        # of the smallest face, plus the volume
        return sum(
            2 * (a + b) + (a * b * c) for a, b, c in (sorted(x) for x in self.input)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
