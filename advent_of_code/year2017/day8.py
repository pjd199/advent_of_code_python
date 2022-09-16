"""Solves the puzzle for Day 8 of Advent of Code 2017.

I Heard You Like Registers

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/8
"""
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Callable, DefaultDict, Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, enum_re, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class _Operator(Enum):
    """Matches the operator in the input."""

    INC = "inc"
    DEC = "dec"


@unique
class _Comparator(Enum):
    """Matches the comparator in the input."""

    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    EQ = "=="
    NOT = "!="


@dataclass
class _Instruction:
    """Represents and instrution in the input."""

    register: str
    operator: _Operator
    value: int
    left: str
    comparator: _Comparator
    right: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 8
    TITLE = "I Heard You Like Registers"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                rf"(?P<register>\w+) (?P<operator>{enum_re(_Operator)}) "
                rf"(?P<value>-?\d+) if (?P<left>\w+) "
                rf"(?P<comparator>{enum_re(_Comparator)}) (?P<right>-?\d+)",
                dataclass_processor(_Instruction),
            ),
        )
        self.max_during = -1
        self.max_end = -1

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if self.max_end == -1:
            self._solve()
        return self.max_end

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if self.max_during == -1:
            self._solve()
        return self.max_during

    def _solve(self) -> None:
        """Solve the puzzle."""
        reg: DefaultDict[str, int] = defaultdict(int)

        compare: Dict[_Comparator, Callable[[_Instruction], bool]] = {
            _Comparator.LT: lambda x: reg[x.left] < x.right,
            _Comparator.GT: lambda x: reg[x.left] > x.right,
            _Comparator.LTE: lambda x: reg[x.left] <= x.right,
            _Comparator.GTE: lambda x: reg[x.left] >= x.right,
            _Comparator.EQ: lambda x: reg[x.left] == x.right,
            _Comparator.NOT: lambda x: reg[x.left] != x.right,
        }

        operate: Dict[_Operator, Callable[[_Instruction], int]] = {
            _Operator.INC: lambda x: reg[x.register] + x.value,
            _Operator.DEC: lambda x: reg[x.register] - x.value,
        }

        self.max_during = 0
        for x in self.input:
            if compare[x.comparator](x):
                reg[x.register] = operate[x.operator](x)
                self.max_during = max(self.max_during, reg[x.register])

        self.max_end = max(reg.values())


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
