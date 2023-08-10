"""Solves the puzzle for Day 5 of Advent of Code 2020.

Binary Boarding

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/5
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 5
    TITLE = "Binary Boarding"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[FBLR]{10}", str_processor))
        self.seats: set[int] = set()

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._find_seat_numbers()
        return max(self.seats)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._find_seat_numbers()
        return next(
            x + 1 for x in self.seats if x + 2 in self.seats and x + 1 not in self.seats
        )

    def _find_seat_numbers(self) -> None:
        """Find the seat numbers."""
        if not self.seats:
            binary_map = {"F": "0", "B": "1", "L": "0", "R": "1"}
            self.seats = {
                int("".join([binary_map[x] for x in seat]), 2) for seat in self.input
            }


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
