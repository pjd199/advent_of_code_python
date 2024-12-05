"""Solves the puzzle for Day 4 of Advent of Code 2024.

Ceres Search

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/4
"""

from collections.abc import Iterable
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 4
    TITLE = "Ceres Search"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[XMAS]+", str_processor)

    def extract(self, locations: Iterable[tuple[int, int]]) -> str:
        """Extract a word from the grid.

        Args:
            locations (Iterable[tuple[int,int]]): the (x,y) locations

        Returns:
            str: the word, with "" for non-existent (x,y)
        """
        return "".join(self.input.get(location, "") for location in locations)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        vectors = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        return sum(
            sum(
                1
                for dx, dy in vectors
                if self.extract((x + i * dx, y + i * dy) for i in range(4)) == "XMAS"
            )
            for x, y in self.input
            if self.input[(x, y)] == "X"
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1
            for x, y in self.input
            if (
                self.input[(x, y)] == "A"
                and all(
                    word in ("MAS", "SAM")
                    for word in (
                        self.extract([(x - 1, y - 1), (x, y), (x + 1, y + 1)]),
                        self.extract([(x - 1, y + 1), (x, y), (x + 1, y - 1)]),
                    )
                )
            )
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
