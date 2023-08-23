"""Solves the puzzle for Day 23 of Advent of Code 2017.

Coprocessor Conflagration

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/23
"""
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, enum_re, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class _Operation(Enum):
    SET = "set"
    SUBTRACT = "sub"
    MULTIPLY = "mul"
    JUMP = "jnz"


@dataclass
class _Instruction:
    op: _Operation
    left: str
    right: str = ""


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 23
    TITLE = "Coprocessor Conflagration"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                rf"(?P<op>{enum_re(_Operation)}) "
                r"(?P<left>[a-z\-0-9]+) ?(?P<right>[a-z\-0-9]+)?",
                dataclass_processor(_Instruction),
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        reg = {x: 0 for x in "abcdefgh"}
        numeric_patch = {
            x.right: int(x.right) for x in self.input if x.right.strip("-").isnumeric()
        }
        reg.update(numeric_patch)

        multiplications = 0

        i = 0
        while 0 <= i < len(self.input):
            op, left, right = self.input[i].op, self.input[i].left, self.input[i].right
            if op == _Operation.SET:
                reg[left] = reg[right]
                i += 1
            elif op == _Operation.SUBTRACT:
                reg[left] -= reg[right]
                i += 1
            elif op == _Operation.MULTIPLY:
                multiplications += 1
                reg[left] *= reg[right]
                i += 1
            elif op == _Operation.JUMP and reg[left] != 0:
                i += reg[right]
            else:
                i += 1

        return multiplications

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        def prime(n: int) -> bool:
            return all(n % i != 0 for i in range(2, n // 2))

        b = (int(self.input[0].right) * 100) + 100000
        c = b + 17000
        return sum(1 for x in range(b, c + 1, 17) if not prime(x))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
