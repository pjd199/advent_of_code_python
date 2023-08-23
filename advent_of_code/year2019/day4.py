"""Solves the puzzle for Day 4 of Advent of Code 2019.

Secure Container

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/4
"""
from pathlib import Path
from re import finditer, search
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 4
    TITLE = "Secure Container"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.lower, self.upper = parse_single_line(
            puzzle_input, r"(\d+)-(\d+)", int_tuple_processor
        )
        self.ready = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._prepare_to_solve()
        return sum(
            1
            for i in self.digits_never_decrease
            if search(r"(\d)\1+", str(i)) is not None
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._prepare_to_solve()
        return sum(
            1
            for i in self.digits_never_decrease
            if any(len(m[0]) == 2 for m in finditer(r"(\d)\1+", str(i)))
        )

    def _prepare_to_solve(self) -> None:
        """Find all the numbers is digits that never decrease."""
        if not self.ready:
            self.digits_never_decrease = [
                i
                for i in range(self.lower, self.upper + 1)
                if all(
                    ((i // (10**x)) % 10) >= ((i // (10 ** (x + 1))) % 10)
                    for x in range(5)
                )
            ]
            self.ready = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
