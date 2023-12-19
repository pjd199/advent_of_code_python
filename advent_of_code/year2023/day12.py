"""Solves the puzzle for Day 12 of Advent of Code 2023.

Hot Springs

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/12
"""
from functools import cache
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    int_processor,
    parse_lines,
    parse_tokens_single_line,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 12
    TITLE = "Hot Springs"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = [
            (
                springs,
                tuple(
                    parse_tokens_single_line(
                        [groups], (r"\d+", int_processor), delimiter=","
                    )
                ),
            )
            for springs, groups in parse_lines(
                puzzle_input, (r"([.?#]+) ([\d,]+)", str_tuple_processor)
            )
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            self.count_solutions(springs, groups) for springs, groups in self.input
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            self.count_solutions("?".join([springs] * 5), groups * 5)
            for springs, groups in self.input
        )

    def count_solutions(self, template: str, groups: tuple[int, ...]) -> int:
        """Count the number of solution.

        Args:
            template (str): the spring template_
            groups (tuple[int, ...]): the spring groups

        Returns:
            int: the result
        """

        @cache
        def find(template: str, groups: tuple[int, ...]) -> int:
            if not template:
                return 0 if groups else 1

            if not groups:
                return 0 if "#" in template else 1

            if template[0] == ".":
                return find(template[1:], groups)

            if template[0] == "#":
                if (
                    len(template) >= groups[0]
                    and all(x in "#?" for x in template[: groups[0]])
                    and (len(template) == groups[0] or template[groups[0]] in ".?")
                ):
                    return find(template[groups[0] + 1 :], groups[1:])
                return 0

            if template[0] == "?":
                return find(f"#{template[1:]}", groups) + find(
                    f".{template[1:]}", groups
                )

            return 0

        return find(template, groups)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
