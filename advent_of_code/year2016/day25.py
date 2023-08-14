"""Solves the puzzle for Day 25 of Advent of Code 2016.

Clock Signal

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/25
"""
from itertools import count
from pathlib import Path
from sys import path
from typing import NoReturn

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))


from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2016.assembunny import load, run_iter


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 25
    TITLE = "Clock Signal"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.program = load(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        clock_pattern = [0, 1] * 5
        result = -1
        for i in count():
            if all(a == b for a, b in zip(run_iter(self.program, a=i), clock_pattern)):
                result = i
                break

        return result

    def solve_part_two(self) -> NoReturn:
        """Solve part two of the puzzle.

        Returns:
            NoReturn: This will never return normally

        Raises:
            NotImplementedError: always!
        """
        raise NotImplementedError


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
