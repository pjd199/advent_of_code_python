"""Solves the puzzle for Day 9 of Advent of Code 2021.

Smoke Basin

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/9
"""
from math import prod
from pathlib import Path
from sys import path

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 9
    TITLE = "Smoke Basin"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r".*", int_processor))
        self.points: dict[tuple[int, int], int] = {}

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._find_low_points()
        return sum(self.points.values()) + len(self.points)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._find_low_points()

        def search(x: int, y: int, found: set[tuple[int, int]]) -> set[tuple[int, int]]:
            moves = [
                (x1, y1)
                for x1, y1 in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
                if (0 <= y1 < len(self.input))
                and (0 <= x1 < len(self.input[y1]))
                and (self.input[y1][x1] != 9)
            ]
            for move in moves:
                if move not in found:
                    found.add(move)
                    search(*move, found)

            return found

        sizes = [len(search(*position, set())) for position in self.points]
        return prod(sorted(sizes)[-3:])

    def _find_low_points(self) -> None:
        if self.points:
            return

        grid = np.pad(
            np.array(self.input), ((1, 1), (1, 1)), constant_values=((10, 10), (10, 10))
        )
        lower_than_above = grid[1:-1, 1:-1] < grid[:-2, 1:-1]
        lower_than_below = grid[1:-1, 1:-1] < grid[2:, 1:-1]
        lower_than_left = grid[1:-1, 1:-1] < grid[1:-1, :-2]
        lower_than_right = grid[1:-1, 1:-1] < grid[1:-1, 2:]

        mask = lower_than_above & lower_than_below & lower_than_left & lower_than_right

        self.points = {
            (x, y): v
            for x, y, v in (
                zip(*np.flip(np.nonzero(mask), axis=0), grid[1:-1, 1:-1][mask])
            )
        }


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
