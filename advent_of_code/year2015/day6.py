"""Solves the puzzle for Day 6 of Advent of Code 2015.

Probably a Fire Hazard

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/6
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from sys import path
from typing import List

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class _Operation(Enum):
    TOGGLE = "toggle"
    ON = "turn on"
    OFF = "turn off"


@dataclass
class _Instruction:
    op: _Operation
    x1: int
    y1: int
    x2: int
    y2: int


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 6
    TITLE = "Probably a Fire Hazard"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        ops = "|".join(x.value for x in _Operation)
        self.input = parse_lines(
            puzzle_input,
            (
                rf"(?P<op>{ops}) "
                r"(?P<x1>\d+),(?P<y1>\d+) through "
                r"(?P<x2>\d+),(?P<y2>\d+)",
                dataclass_processor(_Instruction),
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        lights = np.full((1000, 1000), False)

        for ins in self.input:
            if ins.op == _Operation.ON:
                lights[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.full_like(
                    lights[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)], True
                )
            elif ins.op == _Operation.OFF:
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
            if ins.op == _Operation.ON:
                brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)] = np.add(
                    brightness[ins.y1 : (ins.y2 + 1), ins.x1 : (ins.x2 + 1)], 1
                )
            elif ins.op == _Operation.OFF:
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


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
