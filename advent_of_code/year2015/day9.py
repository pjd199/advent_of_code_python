"""Solves the puzzle for Day 9 of Advent of Code 2015.

All in a Single Night

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/9
"""
from itertools import permutations
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 9
    TITLE = "All in a Single Night"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        tuples = parse_lines(
            puzzle_input,
            (
                r"(?P<a>[A-Za-z]+) to (?P<b>[A-Za-z]+) = (?P<dist>[0-9]+)",
                str_tuple_processor,
            ),
        )

        self.cities = {a for a, _, _ in tuples}
        self.cities.update({b for _, b, _ in tuples})

        self.routes = {(a, b): int(dist) for a, b, dist in tuples}
        self.routes.update({(b, a): int(dist) for a, b, dist in tuples})

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return min(
            sum(map(lambda x, y: self.routes[(x, y)], perm, perm[1:]))
            for perm in permutations(self.cities)
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return max(
            sum(map(lambda x, y: self.routes[(x, y)], perm, perm[1:]))
            for perm in permutations(self.cities)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
