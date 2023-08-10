"""Solves the puzzle for Day 11 of Advent of Code 2021.

Dumbo Octopus

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/11
"""
from pathlib import Path
from sys import path
from typing import Generator, List

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 11
    TITLE = "Dumbo Octopus"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"\d+", int_processor))
        self.cache: list[int] = []

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        it = self._solve()
        return sum(next(it) for i in range(100))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        target = len(self.input) * len(self.input[0])
        return next(
            i + 1 for i, flashes in enumerate(self._solve()) if flashes == target
        )

    def _solve(self) -> Generator[int, None, None]:
        # using caching to improve speed
        if self.cache:
            yield from self.cache
        else:
            self.grid = np.array(self.input)

        while True:
            self.grid += 1
            flashes = 0
            while np.any(self.grid[self.grid > 9]):
                for y, x in np.transpose(np.nonzero(self.grid > 9)):
                    # increase neighbours by 1
                    start_x = 0 if x == 0 else x - 1
                    end_x = x + 1 if x == len(self.grid[y]) - 1 else x + 2
                    start_y = 0 if y == 0 else y - 1
                    end_y = y + 1 if y == len(self.grid) - 1 else y + 2
                    self.grid[start_y:end_y, start_x:end_x] += 1
                    # mark as flashed using a very negative number
                    self.grid[y][x] = np.iinfo(np.int_).min
                    # increament the flash
                    flashes += 1
            # zero all that flashed
            self.grid[self.grid < 0] = 0
            self.cache.append(flashes)
            yield flashes


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
