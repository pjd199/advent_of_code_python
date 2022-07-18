"""Solution for day 6 of Advent of Code 2015."""
from collections import namedtuple
from re import compile
from typing import List

import numpy as np

from advent_of_code.utils.solver_interface import SolverInterface

Instruction = namedtuple("Instruction", "op x1 y1 x2 y2")


class Solver(SolverInterface):
    """Solver for the puzzle."""

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

        self.input = []
        pattern = compile(
            r"(?P<op>toggle|turn on|turn off) "
            r"(?P<x1>\d+),(?P<y1>\d+) through "
            r"(?P<x2>\d+),(?P<y2>\d+)"
        )
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                self.input.append(
                    Instruction(
                        match["op"],
                        int(match["x1"]),
                        int(match["y1"]),
                        int(match["x2"]),
                        int(match["y2"]),
                    )
                )
            else:
                raise RuntimeError(f"Parse error at line {i+1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        lights = np.full((1000, 1000), False)

        for ins in self.input:
            if ins.op == "turn on":
                lights[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.full_like(
                    lights[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)], True
                )
            elif ins.op == "turn off":
                lights[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.full_like(
                    lights[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)], False
                )
            else:  # toggle
                lights[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.logical_not(
                    lights[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)]
                )

        return int(np.count_nonzero(lights))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        brightness = np.full((1000, 1000), 0)

        for ins in self.input:
            if ins.op == "turn on":
                brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.add(
                    brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)], 1
                )
            elif ins.op == "turn off":
                brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.subtract(
                    brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)], 1
                )
                brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.maximum(
                    brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)], 0
                )
            else:  # toggle
                brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.add(
                    brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)], 2
                )

        return int(brightness.sum())
