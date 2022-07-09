"""Solves the puzzle for Day 1 of Advent of Code 2016."""

from collections import namedtuple
from re import compile
from typing import List

from advent_of_code.utils.solver_interface import SolverInterface

Instruction = namedtuple("Instruction", ["turn", "distance"])

class Solver(SolverInterface):
    """Solves the puzzle."""

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

        self.input = []
        pattern = compile(r"(?P<turn>[L|R])(?P<dist>[0-9]+)")
        for i, x in enumerate(tokens):
            if m := pattern.fullmatch(x):
                self.input.append(Instruction(m["turn"], int(m["dist"])))
            else:
                raise RuntimeError(f"Unable to parse line {i}: {x}")

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

        for instruction in self.input:
            if instruction.turn == "L":
                heading = heading - 90 if heading > 0 else 270
            else:
                heading = heading + 90 if heading < 270 else 0

            for _ in range(instruction.distance):
                if heading == 0:
                    y += 1
                elif heading == 90:
                    x += 1
                elif heading == 180:
                    y -= 1
                else:
                    x -= 1

                if (x, y) in breadcrumbs:
                    return abs(x) + abs(y)
                else:
                    breadcrumbs.add((x, y))

        return abs(x) + abs(y)
