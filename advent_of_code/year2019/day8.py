"""Solves the puzzle for Day 8 of Advent of Code 2019.

Space Image Format

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/8
"""
from pathlib import Path
from sys import path
from typing import List

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.ocr import ocr_numpy
from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 8
    TITLE = "Space Image Format"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(puzzle_input, (r"[012]", int_processor))
        self.width = 25
        self.height = 6
        self.size = self.width * self.height

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        layers = np.array(self.input).reshape((len(self.input) // self.size, self.size))
        count_zeros = np.apply_along_axis(lambda x: np.count_nonzero(x == 0), 1, layers)
        best = layers[np.argmin(count_zeros)]
        return np.count_nonzero(best == 1) * np.count_nonzero(best == 2)

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        layers = np.array(self.input).reshape((len(self.input) // self.size, self.size))
        pixels = np.apply_along_axis(
            lambda x: x[np.argmax(x < 2)] if np.nonzero(x < 2) else 0,
            0,
            layers,
        )
        return ocr_numpy(pixels.reshape(self.height, self.width), 1, 0)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
