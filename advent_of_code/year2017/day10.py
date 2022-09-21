"""Solves the puzzle for Day 10 of Advent of Code 2017.

Knot Hash

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/10
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    int_processor,
    parse_single_line,
    parse_tokens_single_line,
    str_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2017.knot_hash import knot_hash


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 10
    TITLE = "Knot Hash"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.int_input = parse_tokens_single_line(
            puzzle_input,
            (r"\d+", int_processor),
            delimiter=",",
        )
        self.str_input = parse_single_line(puzzle_input, r"(\d+,?)+", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        data = list(range(256))

        position = 0
        for skip, length in enumerate(self.int_input):
            section = [data[i % len(data)] for i in range(position, position + length)]
            for i, x in enumerate(reversed(section)):
                data[(position + i) % len(data)] = x
            position += length + skip

        return data[0] * data[1]

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        return knot_hash(self.str_input)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
