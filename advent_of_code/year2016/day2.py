"""Solves the puzzle for Day 2 of Advent of Code 2016.

Bathroom Security

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from enum import Enum, unique
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import enum_processor, enum_re, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 2
    TITLE = "Bathroom Security"

    @unique
    class _Direction(Enum):
        UP = "U"
        DOWN = "D"
        LEFT = "L"
        RIGHT = "R"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input,
            (enum_re(Solver._Direction), enum_processor(Solver._Direction)),
        )

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        return self._find_code(
            {
                (0, 0): "1",
                (1, 0): "2",
                (2, 0): "3",
                (0, 1): "4",
                (1, 1): "5",
                (2, 1): "6",
                (0, 2): "7",
                (1, 2): "8",
                (2, 2): "9",
            }
        )

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        return self._find_code(
            {
                (2, 0): "1",
                (1, 1): "2",
                (2, 1): "3",
                (3, 1): "4",
                (0, 2): "5",
                (1, 2): "6",
                (2, 2): "7",
                (3, 2): "8",
                (4, 2): "9",
                (1, 3): "A",
                (2, 3): "B",
                (3, 3): "D",
                (2, 4): "D",
            }
        )

    def _find_code(self, grid: dict[tuple[int, int], str]) -> str:
        """Find the code, starting at "5".

        Args:
            grid (dict[tuple[int, int], str]): keypad mapping (x, y),
                where (0, 0) is top left

        Returns:
            str: the code
        """
        # find the starting point at "5"
        inverse_grid = {v: k for k, v in grid.items()}
        x, y = inverse_grid["5"]

        # find the code
        code = []
        for line in self.input:
            for direction in line:
                if direction == Solver._Direction.UP and (x, y - 1) in grid:
                    y -= 1
                elif direction == Solver._Direction.DOWN and (x, y + 1) in grid:
                    y += 1
                elif direction == Solver._Direction.LEFT and (x - 1, y) in grid:
                    x -= 1
                elif direction == Solver._Direction.RIGHT and (x + 1, y) in grid:
                    x += 1
            code.append(grid[(x, y)])

        return "".join(code)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
