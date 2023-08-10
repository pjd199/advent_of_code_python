"""Solves the puzzle for Day 6 of Advent of Code 2020.

Custom Customs

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/6
"""
from functools import reduce
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, split_sections, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 6
    TITLE = "Custom Customs"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = [
            [frozenset(line) for line in parse_lines(section, (r"\w+", str_processor))]
            for section in split_sections(puzzle_input)
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(len(reduce(lambda a, b: a | b, group)) for group in self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(len(reduce(lambda a, b: a & b, group)) for group in self.input)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
