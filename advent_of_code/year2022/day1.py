"""Solves the puzzle for Day 1 of Advent of Code 2022.

Calorie Counting

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/1
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 1
    TITLE = "Calorie Counting"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        # parse the input
        delimiter = -1
        lines = parse_lines(
            puzzle_input,
            (r"\d+", int_processor),
            (r"", lambda _: delimiter),
            min_length=3,
        )

        # break the input into a list of lists, one for each elf
        self.input: List[List[int]] = []
        elf: List[int] = []
        for x in lines:
            if x == delimiter:
                self.input.append(elf)
                elf = []
            else:
                elf.append(x)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return max(sum(x) for x in self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(sorted((sum(x) for x in self.input), reverse=True)[0:3])


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
