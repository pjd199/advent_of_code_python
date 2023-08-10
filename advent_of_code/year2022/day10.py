"""Solves the puzzle for Day 10 of Advent of Code 2022.

Cathode-Ray Tube

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/10
"""
from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.ocr import ocr_sequence
from advent_of_code.utils.parser import dataclass_processor, enum_re, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Operator(Enum):
    """Operators from the input."""

    NOOP = "noop"
    ADDX = "addx"


@dataclass
class Instruction:
    """An instruction from the input."""

    op: Operator
    value: int = 0


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 10
    TITLE = "Cathode-Ray Tube"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                rf"(?P<op>{enum_re(Operator)})( (?P<value>-?\d+))?",
                dataclass_processor(Instruction),
            ),
        )
        self.cycles_ready = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.cycles_ready:
            self._solve()

        return sum(i * self.cycles[i - 1] for i in [20, 60, 100, 140, 180, 220])

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        if not self.cycles_ready:
            self._solve()

        return ocr_sequence(
            [
                [
                    "#"
                    if self.cycles[(y * 40) + x] - 1 <= x
                    and x <= self.cycles[(y * 40) + x] + 1
                    else "."
                    for x in range(40)
                ]
                for y in range(6)
            ]
        )

    def _solve(self) -> None:
        """Calculate the register value for each time cycle."""

        def cycle_sequence() -> Generator[int, None, None]:
            yield 1  # initialises register with value 1
            for x in self.input:
                if x.op == Operator.ADDX:
                    yield 0  # wait for a cycle
                yield x.value  # output value

        self.cycles = np.cumsum(np.fromiter(cycle_sequence(), int))
        self.cycles_ready = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
