"""Solves the puzzle for Day 1 of Advent of Code 2016.

No Time for a Taxicab

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from collections import namedtuple
from pathlib import Path
from re import compile
from sys import maxsize, path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface

Instruction = namedtuple("Instruction", ["turn", "distance"])


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 1
    TITLE = "No Time for a Taxicab"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # split up the input
        tokens = puzzle_input[0].split(", ")

        # parse the input
        self.input = []
        pattern = compile(r"(?P<turn>[L|R])(?P<dist>[0-9]+)")
        for i, line in enumerate(tokens):
            match = pattern.fullmatch(line)
            if match:
                self.input.append(Instruction(match["turn"], int(match["dist"])))
            else:
                raise RuntimeError(f"Unable to parse line { i+ 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        x = 0
        y = 0
        heading = 0

        for instruction in self.input:
            if instruction.turn == "L":
                heading = heading - 90 if heading > 0 else 270
            else:
                heading = heading + 90 if heading < 270 else 0

            if heading == 0:
                y += instruction.distance
            elif heading == 90:
                x += instruction.distance
            elif heading == 180:
                y -= instruction.distance
            else:
                x -= instruction.distance

        return abs(x) + abs(y)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        x = 0
        y = 0
        heading = 0
        breadcrumbs = set()

        i = 0
        while i < len(self.input):
            if self.input[i].turn == "L":
                heading = heading - 90 if heading > 0 else 270
            else:
                heading = heading + 90 if heading < 270 else 0

            for _ in range(self.input[i].distance):
                if heading == 0:
                    y += 1
                elif heading == 90:
                    x += 1
                elif heading == 180:
                    y -= 1
                else:
                    x -= 1

                if (x, y) in breadcrumbs:
                    i = maxsize
                    break
                else:
                    breadcrumbs.add((x, y))

            i += 1

        return abs(x) + abs(y)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
