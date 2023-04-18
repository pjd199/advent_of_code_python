"""Solves the puzzle for Day 4 of Advent of Code 2020.

Passport Processing

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/4
"""
from itertools import chain
from pathlib import Path
from re import fullmatch
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_tokens,
    split_sections,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 4
    TITLE = "Passport Processing"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = [
            {
                k: v
                for k, v in chain.from_iterable(
                    parse_tokens(
                        section,
                        (r"(\w{3}):([#\d\w]+)", str_tuple_processor),
                        delimiter=" ",
                        require_delimiter=False,
                    )
                )
            }
            for section in split_sections(puzzle_input)
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(data_validation=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(data_validation=True)

    def _solve(self, data_validation: bool) -> int:
        keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
        eyes = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
        return sum(
            1
            for x in self.input
            if keys <= x.keys()
            and (
                not data_validation
                or (
                    (1920 <= int(x["byr"]) <= 2002)
                    and (2010 <= int(x["iyr"]) <= 2020)
                    and (2020 <= int(x["eyr"]) <= 2030)
                    and (
                        (x["hgt"][-2:] == "cm" and 150 <= int(x["hgt"][:-2]) <= 193)
                        or (x["hgt"][-2:] == "in" and 59 <= int(x["hgt"][:-2]) <= 76)
                    )
                    and fullmatch(r"#[0-9a-z]{6}", x["hcl"])
                    and x["ecl"] in eyes
                    and fullmatch(r"\d{9}", x["pid"])
                )
            )
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
