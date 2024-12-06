"""Solves the puzzle for Day 5 of Advent of Code 2024.

Print Queue

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/5
"""

from functools import cmp_to_key
from itertools import pairwise
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    int_processor,
    int_sequence_processor,
    parse_lines,
    parse_tokens,
    split_sections,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 5
    TITLE = "Print Queue"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        rule_section, update_section = split_sections(puzzle_input, expected_sections=2)
        self.rules = set(
            parse_lines(rule_section, (r"(\d+)\|(\d+)", int_sequence_processor))
        )
        self.updates = parse_tokens(
            update_section, (r"\d+", int_processor), delimiter=","
        )

    def _cmp(self, a: int, b: int) -> int:
        if (a, b) in self.rules:
            return -1
        if (b, a) in self.rules:
            return 1
        return 0

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            update[len(update) // 2]
            for update in self.updates
            if update == sorted(update, key=cmp_to_key(self._cmp))
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            sorted(update, key=cmp_to_key(self._cmp))[len(update) // 2]
            for update in self.updates
            if any(self._cmp(a, b) == 1 for a, b in pairwise(update))
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
