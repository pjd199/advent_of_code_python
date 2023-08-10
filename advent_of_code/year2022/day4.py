"""Solves the puzzle for Day 4 of Advent of Code 2022.

Camp Cleanup

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/4
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 4
    TITLE = "Camp Cleanup"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"(\d+)-(\d+),(\d+)-(\d+)", int_tuple_processor)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1
            for a, b, c, d in self.input
            if set(range(a, b + 1)).issubset(range(c, d + 1))
            or set(range(c, d + 1)).issubset(range(a, b + 1))
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1
            for a, b, c, d in self.input
            if set(range(a, b + 1)).intersection(range(c, d + 1))
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
