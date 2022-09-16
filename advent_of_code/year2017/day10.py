"""Solves the puzzle for Day 10 of Advent of Code 2017.

Knot Hash

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/10
"""
from functools import reduce
from itertools import chain
from operator import xor
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 10
    TITLE = "Knot Hash"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.int_input = parse_tokens(
            puzzle_input, r"\d+", int_processor, delimiter=",", max_length=1
        )[0]
        self.str_input = puzzle_input[0]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        data = list(range(256))

        position = 0
        for skip, length in enumerate(self.int_input):
            section = [data[i % len(data)] for i in range(position, position + length)]
            for i, x in enumerate(reversed(section)):
                data[(position + i) % len(data)] = x
            position += length + skip

        return data[0] * data[1]

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        data = list(range(256))
        position = 0
        skip = 0
        for _ in range(64):
            for length in chain([ord(c) for c in self.str_input], [17, 31, 73, 47, 23]):
                section = [
                    data[i % len(data)] for i in range(position, position + length)
                ]
                for i, x in enumerate(reversed(section)):
                    data[(position + i) % len(data)] = x
                position += length + skip
                skip += 1

        dense_hash = [reduce(xor, data[i : i + 16]) for i in range(0, 256, 16)]

        return "".join(f"{x:02x}" for x in dense_hash)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
