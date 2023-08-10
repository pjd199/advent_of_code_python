"""Solves the puzzle for Day 13 of Advent of Code 2020.

Shuttle Search

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/13
"""
from itertools import count
from math import prod
from operator import itemgetter
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    int_processor,
    parse_lines,
    parse_single_line,
    parse_tokens_single_line,
    str_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 13
    TITLE = "Shuttle Search"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        first_line, second_line = parse_lines(
            puzzle_input, (r".*", str_processor), min_length=2, max_length=2
        )
        self.time = parse_single_line([first_line], r"\d+", int_processor)
        self.buses = parse_tokens_single_line(
            [second_line], (r"\d+", int_processor), (r"x", str_processor), delimiter=","
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        buses = [bus for bus in self.buses if isinstance(bus, int)]
        bus, delay = min(
            [(bus, bus - (self.time % int(bus))) for bus in buses], key=itemgetter(1)
        )
        return bus * delay

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        buses = {i: bus for i, bus in enumerate(self.buses) if isinstance(bus, int)}

        # Solved using the Chinese Remainder Theorom
        b = [(bus - (i % bus)) % bus for i, bus in buses.items()]
        big_n = prod(bus for bus in buses.values())
        n = [big_n // bus for bus in buses.values()]

        x = [
            next(x for x in count(1) if ((ni * x) % bus) == 1)
            for ni, bus in zip(n, buses.values())
        ]
        bnx = map(prod, zip(b, n, x))

        return sum(bnx) % big_n


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
