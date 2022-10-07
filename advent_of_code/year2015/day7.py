"""Solves the puzzle for Day 7 of Advent of Code 2015.

Some Assembly Required

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/7
"""
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Callable, Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class _Operator(Enum):
    AND = "AND"
    OR = "OR"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    NOT = "NOT"


@dataclass
class _Expression:
    output: str


@dataclass
class _Signal(_Expression):
    signal: int


@dataclass
class _Connection(_Expression):
    input_wire: str


@dataclass
class _Operation(_Expression):
    operator: _Operator
    right: str
    left: str = ""


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 7
    TITLE = "Some Assembly Required"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        parsed = parse_lines(
            puzzle_input,
            (
                r"(?P<signal>[0-9]+) -> (?P<output>[a-z]+)",
                dataclass_processor(_Signal),
            ),
            (
                r"(?P<input_wire>[a-z]+) -> (?P<output>[a-z]+)",
                dataclass_processor(_Connection),
            ),
            (
                r"((?P<left>[a-z]+|[0-9]+) )?"
                r"(?P<operator>AND|OR|LSHIFT|RSHIFT|NOT) "
                r"(?P<right>[a-z]+|[0-9]+) -> "
                r"(?P<output>[a-z]+)",
                dataclass_processor(_Operation),
            ),
        )

        self.wiring_diagram: Dict[str, _Expression] = {x.output: x for x in parsed}
        self.part_one = -1
        self.part_two = -1

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if self.part_one == -1:
            self.part_one = self._resolve("a", {})
        return self.part_one

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if self.part_one == -1:
            self.part_one = self._resolve("a", {})

        if self.part_two == -1:
            self.wiring_diagram["b"] = _Signal("b", self._resolve("a", {}))
            self.part_two = self._resolve("a", {})

        return self.part_two

    def _resolve(
        self,
        wire: str,
        cache: Dict[str, int],
    ) -> int:
        """Recursively resolves the signal on the request wire.

        Resolves the signal on the request wire, recursively nagivating the
        wiring_diagram to evaluate all the expressions. Uses a cache so that
        each expression is only evaluated once, minimising recursions

        Args:
            wire (str): the wire to resolve
            cache (Dict[str, int]): a cache of resolved results

        Returns:
            int: the final value of the wire
        """
        # if this is just a simple number, return the number as an int
        if isinstance(wire, str) and wire.isnumeric():
            return int(wire)

        # if this is not yet been cached, resolved the expression
        if wire not in cache:
            expression = self.wiring_diagram[wire]

            if isinstance(expression, _Signal):
                cache[wire] = int(expression.signal)

            elif isinstance(expression, _Connection):
                cache[wire] = self._resolve(expression.input_wire, cache)

            elif isinstance(expression, _Operation):
                operations: Dict[_Operator, Callable[[str, str], int]] = {
                    _Operator.AND: lambda a, b: (
                        self._resolve(a, cache) & self._resolve(b, cache)
                    ),
                    _Operator.OR: lambda a, b: (
                        self._resolve(a, cache) | self._resolve(b, cache)
                    ),
                    _Operator.LSHIFT: lambda a, b: (
                        self._resolve(a, cache) << self._resolve(b, cache)
                    ),
                    _Operator.RSHIFT: lambda a, b: (
                        self._resolve(a, cache) >> self._resolve(b, cache)
                    ),
                    _Operator.NOT: lambda _, b: ~self._resolve(b, cache),
                }
                cache[wire] = operations[expression.operator](
                    expression.left, expression.right
                )

        # return the resolved value
        return cache[wire]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
