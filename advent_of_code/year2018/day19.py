"""Solves the puzzle for Day 19 of Advent of Code 2018.

Go With The Flow

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/19
"""
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from sys import maxsize, path

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    dataclass_processor,
    int_processor_group,
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
    DAY = 19
    TITLE = "Go With The Flow"

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
            puzzle_input[0:1], r"#ip (\d)", int_processor_group(1)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        registers = [0, 0, 0, 0, 0, 0]
        self._solve(registers)
        return registers[0]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # input program finds the sum of the factors of a number,
        # but is very slow, so break when the number is found,
        # and use numpy to calculate the answer instead
        registers = [1, 0, 0, 0, 0, 0]
        self._solve(registers, break_at_line=1)

        number = registers[-1]

        # find the sum of the factors of "number"
        array = np.arange(1, number + 1)  # offset to avoid div by zero
        modulo = np.mod(number, array)
        factors_with_offset = np.where(modulo == 0)
        factors = np.add(factors_with_offset, 1)  # remove offset
        return int(np.sum(factors))

    def _solve(self, registers: list[int], break_at_line: int = maxsize) -> None:
        program = deepcopy(self.input)

        self.actions: dict[str, Callable[[tuple[int, ...], Instruction], int]] = {
            "addr": lambda r, i: r[i.a] + r[i.b],
            "addi": lambda r, i: r[i.a] + i.b,
            "mulr": lambda r, i: r[i.a] * r[i.b],
            "muli": lambda r, i: r[i.a] * i.b,
            "banr": lambda r, i: r[i.a] & r[i.b],
            "bani": lambda r, i: r[i.a] & i.b,
            "borr": lambda r, i: r[i.a] | r[i.b],
            "bori": lambda r, i: r[i.a] | i.b,
            "setr": lambda r, i: r[i.a],
            "seti": lambda _, i: i.a,
            "gtir": lambda r, i: 1 if i.a > r[i.b] else 0,
            "gtri": lambda r, i: 1 if r[i.a] > i.b else 0,
            "gtrr": lambda r, i: 1 if r[i.a] > r[i.b] else 0,
            "eqir": lambda r, i: 1 if i.a == r[i.b] else 0,
            "eqri": lambda r, i: 1 if r[i.a] == i.b else 0,
            "eqrr": lambda r, i: 1 if r[i.a] == r[i.b] else 0,
        }
        pointer = 0
        while 0 <= pointer < len(program) and pointer != break_at_line:
            registers[self.instruction_pointer] = pointer
            instruction = program[pointer]
            registers[instruction.c] = self.actions[instruction.opcode](
                tuple(registers), instruction
            )
            pointer = registers[self.instruction_pointer]
            pointer += 1


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
