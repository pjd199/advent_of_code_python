"""Solution for day 20 of Advent of Code 2015."""
from pathlib import Path
from re import fullmatch
from sys import path
from typing import List

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 20
    TITLE = "Infinite Elves and Infinite Houses"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if puzzle_input is None or len(puzzle_input) == 0:
            raise RuntimeError("Puzzle input is empty")

        if len(puzzle_input) == 1 and fullmatch(r"[0-9]+", puzzle_input[0]):
            self.target = int(puzzle_input[0])
        else:
            raise RuntimeError("Expected a number on line 1")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        result = -1
        limit = 1000000
        houses = np.zeros(limit)
        for elf in range(1, limit):
            houses[elf::elf] += elf * 10
            if houses[elf] >= self.target:
                result = elf
                break

        return result

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle

        limit = 1000000
        result = -1
        houses = np.zeros(limit)
        for elf in range(1, limit):
            houses[elf : elf * 50 : elf] += elf * 11
            if houses[elf] >= self.target:
                result = elf
                break

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
