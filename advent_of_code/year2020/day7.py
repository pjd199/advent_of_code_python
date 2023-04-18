"""Solves the puzzle for Day 7 of Advent of Code 2020.

Handy Haversacks

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/7
"""
from functools import lru_cache
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    parse_tokens_single_line,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 7
    TITLE = "Handy Haversacks"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = {
            k: {
                k: v
                for v, k in parse_tokens_single_line(
                    [v],
                    (r"(\d+) (\w+ \w+) bags?", str_tuple_processor),
                    delimiter=", ",
                    require_delimiter=False,
                )
            }
            if v != "no other bags"
            else {}
            for k, v in parse_lines(
                puzzle_input,
                (r"(\w+ \w+) bags contain ([\d\w, ]+).", str_tuple_processor),
            )
        }

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """

        @lru_cache(maxsize=len(self.input))
        def find_shiny_bags(bag: str) -> bool:
            return (bag == "shiny gold") or any(
                find_shiny_bags(b) for b in self.input[bag]
            )

        return sum(
            1 for bag in self.input if bag != "shiny gold" and find_shiny_bags(bag)
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        @lru_cache(maxsize=len(self.input))
        def bag_count(bag: str) -> int:
            return 1 + sum((int(n) * bag_count(b)) for b, n in self.input[bag].items())

        return bag_count("shiny gold") - 1


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
