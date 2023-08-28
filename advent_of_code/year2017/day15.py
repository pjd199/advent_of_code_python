"""Solves the puzzle for Day 15 of Advent of Code 2017.

Dueling Generators

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/15
"""
from collections.abc import Iterator
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor_group, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 15
    TITLE = "Dueling Generators"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.seed_a, self.seed_b = parse_lines(
            puzzle_input, (r"Generator [AB] starts with (\d+)", int_processor_group(1))
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        iter_a = self._generator(self.seed_a, 16807)
        iter_b = self._generator(self.seed_b, 48271)
        return sum(
            1
            for _ in range(40000000)
            if (next(iter_a) & 65535) == (next(iter_b) & 65535)
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        iter_a = self._generator(self.seed_a, 16807, 4)
        iter_b = self._generator(self.seed_b, 48271, 8)
        return sum(
            1
            for _ in range(5000000)
            if (next(iter_a) & 65535) == (next(iter_b) & 65535)
        )

    def _generator(self, seed: int, factor: int, modulo: int = 1) -> Iterator[int]:
        """Simulate the Generator in the puzzle.

        Args:
            seed (int): starting value
            factor (int): multiplier factor
            modulo (int): Only return results multiples of modulo. Defaults to 1.

        Yields:
            int: the next number in the sequence
        """
        value = seed
        if modulo == 1:
            while True:
                value = (value * factor) % 2147483647
                yield value
        else:
            while True:
                value = (value * factor) % 2147483647
                if value % modulo == 0:
                    yield value


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
