"""Solves the puzzle for Day 1 of Advent of Code 2018.

Chronal Calibration

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/1
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 1
    TITLE = "Chronal Calibration"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[+-]\d+", int_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        total = 0
        result = -1
        seen = set()
        i = 0
        while True:
            total += self.input[i]
            i = (i + 1) % len(self.input)
            if total in seen:
                result = total
                break
            else:
                seen.add(total)

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
