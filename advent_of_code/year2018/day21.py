"""Solves the puzzle for Day 21 of Advent of Code 2018.

Chronal Conversion

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/21
"""
from dataclasses import dataclass
from pathlib import Path
from sys import path
from time import perf_counter

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    dataclass_processor,
    parse_lines,
    parse_single_line,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Instruction:
    """An instruction read from the input."""

    opcode: str
    a: int
    b: int
    c: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 21
    TITLE = "Chronal Conversion"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        # parse the program
        self.input = parse_lines(
            puzzle_input,
            (
                r"(?P<opcode>[a-z]+) (?P<a>\d+) (?P<b>\d+) (?P<c>\d+)",
                dataclass_processor(Instruction),
            ),
            header=(r"#ip \d",),
            min_length=2,
        )
        # parse the instruction pointer
        self.instruction_pointer = parse_single_line(
            puzzle_input[0:1], r"#ip (\d)", lambda m: int(m[1])
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(True)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(False)

    def _solve(self, part_one: bool) -> int:
        """Solve the puzzle, but with a handcoded transpiled version of the program.

        Args:
            part_one (bool): toggles result for part one and part two

        Returns:
            int: the result
        """
        input_number = self.input[7].a

        # part two never ends, so terminate after a 1s timeout
        timeout_duration = 1.0
        timeout = perf_counter() + timeout_duration

        # registers
        r = [0, 0, 0, 0, 0, 0, 0]

        possibilities = set()
        result = -1
        complete = False
        while not complete:
            r[2] = r[3] | 65536
            r[3] = input_number
            while not complete:
                r[1] = r[2] & 255
                r[3] += r[1]
                r[3] &= 16777215
                r[3] *= 65899
                r[3] &= 16777215
                if 256 > r[2]:
                    if part_one:
                        result = r[3]
                        complete = True
                    else:
                        if r[3] not in possibilities:
                            possibilities.add(r[3])
                            timeout = perf_counter() + timeout_duration
                            result = r[3]
                        if perf_counter() > timeout:
                            complete = True
                    break
                r[2] //= 256
                r[1] = r[2]

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
