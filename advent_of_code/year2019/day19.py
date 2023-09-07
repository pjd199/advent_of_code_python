"""Solves the puzzle for Day 19 of Advent of Code 2019.

Tractor Beam

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/19
"""
from collections.abc import Iterator
from itertools import count
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 19
    TITLE = "Tractor Beam"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.computer = IntcodeComputer(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        count = 0
        for (y, x1), (_, x2) in zip(self._lower_edge(), self._upper_edge()):
            if x1 < 50 and y < 50:
                count += min(x2, 49) - x1 + 1
            else:
                break
        return count

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return next(
            (x * 10000) + (y - 99)
            for y, x in self._lower_edge()
            if y >= 99 and self._tractor_beam(x + 99, y - 99)
        )

    def _tractor_beam(self, x: int, y: int) -> bool:
        """Look for the tractor beam.

        Args:
            x (int): x co-ordinate
            y (int): y co-ordinate

        Returns:
            bool: True if co-ordinate in tractor beam, else False
        """
        self.computer.reset()
        self.computer.input_data(x, y)
        self.computer.execute()
        return self.computer.read_output() == 1

    def _lower_edge(self) -> Iterator[tuple[int, int]]:
        """Iterator for the lower edge of the tractor beam.

        Yields:
            tuple[int, int]: Iterator of (x,y) co-ordinates
        """
        x = 0
        for y in count():
            for x1 in range(x, x + 5):
                if self._tractor_beam(x1, y):
                    x = x1
                    yield y, x
                    break

    def _upper_edge(self) -> Iterator[tuple[int, int]]:
        """Iterator for the upper edge of the tractor beam.

        Yields:
            tuple[int, int]: Iterator of (x,y) co-ordinates
        """
        x = 0
        for y in count():
            for x1 in range(x, x + 5):
                if self._tractor_beam(x1, y) and not self._tractor_beam(x1 + 1, y):
                    x = x1
                    yield y, x
                    break


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
