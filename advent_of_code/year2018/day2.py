"""Solves the puzzle for Day 2 of Advent of Code 2018.

Inventory Management System

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/2
"""
from itertools import combinations, groupby
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 2
    TITLE = "Inventory Management System"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[a-z]+", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        pairs = 0
        triples = 0

        for line in self.input:
            for _, g in groupby(sorted(line)):
                if len(list(g)) == 2:
                    pairs += 1
                    break

        for line in self.input:
            for _, g in groupby(sorted(line)):
                if len(list(g)) == 3:
                    triples += 1
                    break

        return pairs * triples

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        result = ""

        for a, b in combinations(self.input, 2):
            matching = "".join(
                [a for a, _ in filter(lambda x: x[0] == x[1], zip(a, b))]
            )
            if len(matching) == len(a) - 1:
                result = matching
                break

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
