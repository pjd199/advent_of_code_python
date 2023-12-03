"""Solves the puzzle for Day 3 of Advent of Code 2023.

Gear Ratios

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/3
"""
from collections.abc import Iterator
from math import prod
from pathlib import Path
from re import finditer
from string import digits, punctuation
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 3
    TITLE = "Gear Ratios"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        special = digits + punctuation.replace(".", "")
        grid = parse_grid(puzzle_input, rf"[0-9.{special}]", str_processor)
        self.numbers = {
            (m.start(), i): m[0]
            for i, line in enumerate(puzzle_input)
            for m in finditer(r"\d+", line)
        }
        self.symbols = {(x, y): v for (x, y), v in grid.items() if v in special}

    def border(self, x: int, y: int) -> Iterator[tuple[int, int]]:
        """Iterate the co-ordinates of the border around the number.

        Args:
            x (int): x co-ordinate
            y (int): y co-ordinate

        Yields:
            tuple[int, int]: the iterator
        """
        number = self.numbers[(x, y)]
        yield from (
            {(x2, y - 1) for x2 in range(x - 1, x + len(number) + 1)}
            | {(x - 1, y), (x + len(number), y)}
            | {(x2, y + 1) for x2 in range(x - 1, x + len(number) + 1)}
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            int(number)
            for (x, y), number in self.numbers.items()
            if any((bx, by) in self.symbols for bx, by in self.border(x, y))
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        adjacent: dict[tuple[int, int], list[int]] = {
            (x, y): [] for (x, y), v in self.symbols.items() if v == "*"
        }
        for (x, y), number in self.numbers.items():
            for bx, by in self.border(x, y):
                if (bx, by) in adjacent:
                    adjacent[(bx, by)].append(int(number))

        return sum(prod(numbers) for numbers in adjacent.values() if len(numbers) == 2)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
