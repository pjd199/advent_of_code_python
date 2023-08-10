"""Solves the puzzle for Day 2 of Advent of Code 2017.

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/2
"""
from itertools import permutations
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 2
    TITLE = "Corruption Checksum"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"\d+", int_processor), delimiter="\t")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(max(row) - min(row) for row in self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            a // b for row in self.input for a, b in permutations(row, 2) if a % b == 0
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
