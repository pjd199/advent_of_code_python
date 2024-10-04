"""Solves the puzzle for Day 1 of Advent of Code 2023.

Trebuchet?!

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/1
"""

from collections.abc import Iterator
from pathlib import Path
from re import findall
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 1
    TITLE = "Trebuchet?!"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[a-z0-9]+", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self.extact_values(numbers_as_words=False))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self.extact_values(numbers_as_words=True))

    def extact_values(self, numbers_as_words: bool) -> Iterator[int]:
        """Extract the digits from the input.

        Args:
            numbers_as_words (bool): Treat number words as digits

        Yields:
            int: the extacted digits
        """
        lookup = {str(i): i for i in range(10)}
        if numbers_as_words:
            lookup |= {
                "zero": 0,
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9,
            }
        for line in self.input:
            digits = findall(rf"(?=({" | ".join(lookup)}))", line)
            if digits:
                yield lookup[digits[0]] * 10 + lookup[digits[-1]]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
