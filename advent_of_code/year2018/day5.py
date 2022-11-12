"""Solves the puzzle for Day 5 of Advent of Code 2018.

Alchemical Reduction

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/5
"""
from pathlib import Path
from string import ascii_lowercase, ascii_uppercase
from sys import maxsize, path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 5
    TITLE = "Alchemical Reduction"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"[a-zA-Z]+", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return len(self._react(list(self.input)))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        lowest = maxsize
        for lower, upper in zip(ascii_lowercase, ascii_uppercase):
            lowest = min(lowest, len(self._react(list(self.input), f"{lower}{upper}")))

        return lowest

    def _react(self, polymer: List[str], remove: str = "") -> List[str]:
        """Perform a polymer reaction.

        Args:
            polymer (List[str]): The polymer to react
            remove (str): any types to ignore

        Returns:
            List[str]: the result
        """
        result = list(polymer)
        i = 0
        while i < len(result) - 1:
            if result[i] in remove:
                result.pop(i)
                i = max(0, i - 1)
            if result[i].lower() == result[i + 1].lower() and (
                (result[i].islower() and result[i + 1].isupper())
                or (result[i].isupper() and result[i + 1].islower())
            ):
                result.pop(i + 1)
                result.pop(i)
                i = max(0, i - 1)
            else:
                i += 1
        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
