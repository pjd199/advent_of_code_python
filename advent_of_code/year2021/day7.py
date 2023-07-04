"""Solves the puzzle for Day 7 of Advent of Code 2021.

The Treachery of Whales

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/7
"""
from pathlib import Path
from sys import path
from typing import List

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 7
    TITLE = "The Treachery of Whales"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"\d+", int_processor), delimiter=","
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        least = np.iinfo(np.int32).max
        positions = np.array(self.input)
        for i in positions:
            distances = np.abs(positions - i)
            fuel = np.sum(distances)
            if fuel < least:
                least = fuel
        return int(least)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        least = np.iinfo(np.int32).max
        positions = np.array(self.input)
        for i in range(np.max(positions)):
            distances = np.abs(positions - i)
            fuel = np.sum((distances * (distances + 1)) // 2)
            if fuel < least:
                least = fuel
        return int(least)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
