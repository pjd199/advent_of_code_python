"""Solves the puzzle for Day 8 of Advent of Code 2023.

Haunted Wasteland

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/8
"""
from collections.abc import Iterator
from itertools import cycle
from math import lcm
from pathlib import Path
from re import match
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

    YEAR = 2023
    DAY = 8
    TITLE = "Haunted Wasteland"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input)
        self.instructions = parse_single_line(sections[0], "[LR]+", str_processor)
        self.nodes = {
            root: (left, right)
            for root, left, right in parse_lines(
                sections[1],
                (
                    r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)",
                    str_tuple_processor,
                ),
            )
        }

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self.distance("AAA", "ZZZ")

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return lcm(
            *(
                self.distance(location, r"..Z")
                for location in [n for n in self.nodes if match(r"..A", n)]
            )
        )

    def distance(self, start: str, finish: str) -> int:
        """Find the distance from the start to the finish.

        Args:
            start (str): starting pattern
            finish (str): finishing pattern

        Returns:
            int: the distance
        """

        def locations() -> Iterator[str]:
            location = start
            for instruction in cycle(list(self.instructions)):
                yield location
                location = self.nodes[location][0 if instruction == "L" else 1]

        return next(
            steps
            for steps, location in enumerate(locations())
            if match(finish, location)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
