"""Solves the puzzle for Day 4 of Advent of Code 2017.

High-Entropy Passphrases

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/4
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 4
    TITLE = "High-Entropy Passphrases"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input, (r"[a-z]+", str_processor), delimiter=" "
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(1 for line in self.input if len(set(line)) == len(line))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1
            for line in self.input
            if len({str(sorted(word)) for word in line}) == len(line)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
