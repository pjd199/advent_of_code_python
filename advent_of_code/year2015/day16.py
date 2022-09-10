"""Solves the puzzle for Day 16 of Advent of Code 2015.

Aunt Sue

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/16
"""
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

    UNKNOWN_SUE = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    YEAR = 2015
    DAY = 16
    TITLE = "Aunt Sue"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.list_of_sues = [
            {
                a: int(a_val),
                b: int(b_val),
                c: int(c_val),
            }
            for a, a_val, b, b_val, c, c_val in parse_lines(
                puzzle_input,
                (
                    r"Sue [0-9]+: "
                    r"(?P<a>[a-z]+): (?P<a_val>[0-9]+), "
                    r"(?P<b>[a-z]+): (?P<b_val>[0-9]+), "
                    r"(?P<c>[a-z]+): (?P<c_val>[0-9]+)",
                    str_tuple_processor,
                ),
            )
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # solve part one
        result = -1
        for i, sue in enumerate(self.list_of_sues):
            if all([int(v) == Solver.UNKNOWN_SUE[k] for k, v in sue.items()]):
                result = i + 1
                break

        return result

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        result = -1
        for i, sue in enumerate(self.list_of_sues):
            matches = []
            for k, v in sue.items():
                if k == "cats" or k == "trees":
                    matches.append(int(v) > Solver.UNKNOWN_SUE[k])
                elif k == "pomeranians" or k == "goldfish":
                    matches.append(int(v) < Solver.UNKNOWN_SUE[k])
                else:
                    matches.append(int(v) == Solver.UNKNOWN_SUE[k])
            if all(matches):
                result = i + 1
                break

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
