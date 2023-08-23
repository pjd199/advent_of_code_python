"""Solves the puzzle for Day 13 of Advent of Code 2017.

Packet Scanners

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/13
"""
from itertools import count
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 13
    TITLE = "Packet Scanners"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = dict(
            parse_lines(
                puzzle_input,
                (
                    r"(?P<depth>\d+): (?P<range>\d+)",
                    lambda m: (int(m["depth"]), int(m["range"])),
                ),
            )
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            depth * length
            for depth, length in self.input.items()
            if depth % (2 * (length - 1)) == 0
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return next(
            delay
            for delay in count()
            if not any(
                (delay + depth) % (2 * (length - 1)) == 0
                for depth, length in self.input.items()
            )
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
