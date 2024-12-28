"""Solves the puzzle for Day 19 of Advent of Code 2024.

Linen Layout

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/19
"""

from functools import cache

from advent_of_code.utils.parser import (
    parse_lines,
    parse_tokens_single_line,
    split_sections,
    str_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 19
    TITLE = "Linen Layout"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        patterns, designs = split_sections(puzzle_input, expected_sections=2)

        self.patterns = parse_tokens_single_line(
            patterns, (r"[a-z]+", str_processor), delimiter=", "
        )
        self.designs = parse_lines(designs, (r"[a-z]+", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """

        @cache
        def valid(design: str) -> bool:
            if design == "":
                return True
            for pattern in self.patterns:
                if design.startswith(pattern) and valid(design.removeprefix(pattern)):
                    return True
            return False

        return sum(1 for design in self.designs if valid(design))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        @cache
        def count(design: str) -> int:
            if design == "":
                return 1
            total = 0
            for pattern in self.patterns:
                if design.startswith(pattern):
                    total += count(design.removeprefix(pattern))
            return total

        return sum(count(design) for design in self.designs)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
