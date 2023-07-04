"""Solves the puzzle for Day 14 of Advent of Code 2021.

Extended Polymerization

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/14
"""
from collections import Counter
from functools import lru_cache
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    parse_single_line,
    split_sections,
    str_processor,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 14
    TITLE = "Extended Polymerization"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input, expected_sections=2)
        self.template = parse_single_line(sections[0], r"[A-Z]+", str_processor)
        self.rules: dict[str, str] = {
            k: v
            for k, v in parse_lines(
                sections[1], (r"([A-Z]+) -> ([A-Z]+)", str_tuple_processor)
            )
        }

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(10)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(40)

    def _solve(self, max_steps: int) -> int:
        """Solve the puzzle.

        Args:
            max_steps (int): number of steps to process

        Returns:
            int: the result
        """

        @lru_cache(maxsize=len(self.rules) * max_steps)
        def count(left: str, right: str, step: int = 0) -> Counter[str]:
            element = self.rules[left + right]
            new_counter = Counter(element)
            if step + 1 < max_steps:
                new_counter.update(count(left, element, step + 1))
                new_counter.update(count(element, right, step + 1))
            return new_counter

        # start the cached recusion to count the final number of elements
        counter = Counter(self.template)
        for left, right in zip(self.template, self.template[1:]):
            counter.update(count(left, right))

        # return the result
        most_common, *_, least_common = [i for _, i in counter.most_common()]
        return most_common - least_common


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
