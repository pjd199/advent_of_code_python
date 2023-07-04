"""Solves the puzzle for Day 13 of Advent of Code 2021.

Transparent Origami

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/13
"""
from pathlib import Path
from sys import path
from typing import List

import numpy as np
from numpy.typing import NDArray

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.ocr import ocr_numpy
from advent_of_code.utils.parser import int_tuple_processor, parse_lines, split_sections
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 13
    TITLE = "Transparent Origami"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input)
        self.marks = parse_lines(sections[0], (r"(\d+),(\d+)", int_tuple_processor))
        self.folds = parse_lines(
            sections[1],
            (r"fold along y=(\d+)", lambda m: (0, int(m[1]))),
            (r"fold along x=(\d+)", lambda m: (int(m[1]), 0)),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return np.count_nonzero(self._fold(fold_once=True))

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        return ocr_numpy(self._fold(), fill_pixel=True, empty_pixel=False)

    def _fold(self, fold_once: bool = False) -> NDArray[np.bool_]:
        """Fold the paper as instructed.

        Args:
            fold_once (bool): if True, only folds once

        Returns:
            NDArray[np.bool_]: the folded array
        """
        # put all the marks on a grid
        max_x, max_y = (max(a) for a in zip(*self.marks))
        grid = np.full((max_y + 1, max_x + 1), fill_value=False)
        col_indices, row_indices = zip(*self.marks)
        grid[(row_indices, col_indices)] = True

        for x, y in self.folds:
            if x == 0:
                # fold along a horizontal line
                grid = np.logical_or(grid[:y], grid[-1:y:-1])
            elif y == 0:
                # fold along a vertical line
                grid = np.logical_or(grid[:, :x], grid[:, -1:x:-1])
            if fold_once:
                break
        return grid


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
