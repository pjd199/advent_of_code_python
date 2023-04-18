"""Solves the puzzle for Day 6 of Advent of Code 2022.

Tuning Trouble

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/6
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 6
    TITLE = "Tuning Trouble"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"[a-z]+", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(4)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(14)

    def _solve(self, length: int) -> int:
        """Solve the puzzle.

        Args:
            length (int): length of unique character sequence

        Returns:
            int: number of letters until sequence found
        """
        result = -1
        for i in range(length, len(self.input)):
            if len(set(self.input[i - length : i])) == length:
                result = i
                break

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
