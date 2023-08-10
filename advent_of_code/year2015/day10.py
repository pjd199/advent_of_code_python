"""Solves the puzzle for Day 10 of Advent of Code 2015.

Elves Look, Elves Say

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/10
"""
from itertools import groupby
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 10
    TITLE = "Elves Look, Elves Say"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file

        """
        self.puzzle_input = parse_single_line(puzzle_input, r"\d+", str_processor)

        self.part_one_seq = ""

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.part_one_seq = self._run(self.puzzle_input, 40)
        return len(self.part_one_seq)

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self.solve_part_one()

        return len(self._run(self.part_one_seq, 10))

    def _run(self, seq: str, cycles: int) -> str:
        """Run the solution.

        Args:
            seq (str): input sequence
            cycles (int): number of cycles to complete

        Returns:
            str: the output sequence
        """
        for _ in range(cycles):
            seq = "".join(str(len(list(g))) + k for k, g in groupby(seq))
        return seq


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
