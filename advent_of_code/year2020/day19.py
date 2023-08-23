"""Solves the puzzle for Day 19 of Advent of Code 2020.

Monster Messages

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/19
"""
from functools import lru_cache
from pathlib import Path
from re import fullmatch
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    split_sections,
    str_processor,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 19
    TITLE = "Monster Messages"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input, expected_sections=2)
        self.rules = {
            k: v.strip('"')
            for k, v in parse_lines(
                sections[0], (r"(\d+): ([0-9| ]+|\"[ab]\")", str_tuple_processor)
            )
        }
        self.messages = parse_lines(sections[1], (r"[ab]+", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(modify_rules=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(modify_rules=True)

    def _solve(self, modify_rules: bool) -> int:
        rules = self.rules.copy()
        if modify_rules:
            rules["8"] = "42 | 42 8"
            rules["11"] = "42 31 | 42 11 31"

        @lru_cache(maxsize=len(self.rules))
        def resolve(key: str) -> str:
            rule = rules[key]
            if rule == "a" or rule == "b":
                return rule
            if key == "8" and modify_rules:
                return f"({resolve('42')}+)"
            if key == "11" and modify_rules:
                repititions = [
                    f"{resolve('42')}{{{x}}}{resolve('31')}{{{x}}}"
                    for x in range(1, 10)  # guestimate of 10 for max repititions
                ]
                return f"({'|'.join(repititions)})"
            content = ["|" if t == "|" else resolve(t) for t in rule.split(" ")]
            return f"({''.join(content)})"

        return sum(1 for message in self.messages if fullmatch(resolve("0"), message))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
