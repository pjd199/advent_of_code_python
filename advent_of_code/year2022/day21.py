"""Solves the puzzle for Day 21 of Advent of Code 2022.

Monkey Math

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/21
"""
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from operator import add, floordiv, mul, sub
from pathlib import Path
from sys import path
from typing import cast

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Expression:
    """An expression from the input."""

    name: str
    left: str
    operator: str
    right: str


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 21
    TITLE = "Monkey Math"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input: dict[str, int | Expression] = dict(
            parse_lines(
                puzzle_input,
                (
                    r"(?P<name>[a-z]+): "
                    r"(?P<left>[a-z]+) (?P<operator>[\+\-\*\/]) (?P<right>[a-z]+)",
                    lambda m: (
                        m["name"],
                        Expression(m["name"], m["left"], m["operator"], m["right"]),
                    ),
                ),
                (
                    r"(?P<name>[a-z]+): (?P<value>[0-9]+)",
                    lambda m: (m["name"], int(m["value"])),
                ),
            )
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve("root", self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # functions to rearrange the formulee
        rearrange_left: dict[str, Callable[[Expression], Expression]] = {
            "+": lambda x: Expression(x.left, x.name, "-", x.right),
            "-": lambda x: Expression(x.left, x.name, "+", x.right),
            "*": lambda x: Expression(x.left, x.name, "/", x.right),
            "/": lambda x: Expression(x.left, x.name, "*", x.right),
        }

        rearrange_right: dict[str, Callable[[Expression], Expression]] = {
            "+": lambda x: Expression(x.right, x.name, "-", x.left),
            "-": lambda x: Expression(x.right, x.left, "-", x.name),
            "*": lambda x: Expression(x.right, x.name, "/", x.left),
            "/": lambda x: Expression(x.right, x.left, "/", x.name),
        }

        # generate the route from root to human
        route_to_human = self._route_to_human()

        # rearrange the root equation to find equality
        expressions = deepcopy(self.input)
        root = cast(Expression, expressions.pop("root"))
        expressions["root"] = 0
        new_root = Expression("root", root.left, "-", root.right)

        if new_root.left in route_to_human:
            expressions[new_root.left] = rearrange_left[new_root.operator](new_root)
        else:  # pragma: no cover
            expressions[new_root.right] = rearrange_right[new_root.operator](new_root)

        # rearrange the formulee on the path between root and human
        for current in route_to_human[1:-1]:
            exp = cast(Expression, self.input[current])
            if exp.left in route_to_human:
                expressions[exp.left] = rearrange_left[exp.operator](exp)
            else:
                expressions[exp.right] = rearrange_right[exp.operator](exp)

        # solve the equation for humn
        return self._solve("humn", expressions)

    def _solve(self, current: str, expressions: dict[str, int | Expression]) -> int:
        """Solve the equations.

        Args:
            current (str): _description_
            expressions (dict[str, int | Expression]): _description_

        Returns:
            int: _description_
        """
        operators: dict[str, Callable[[int, int], int]] = {
            "+": add,
            "-": sub,
            "*": mul,
            "/": floordiv,
        }

        exp = expressions[current]
        if isinstance(exp, Expression):
            left = self._solve(exp.left, expressions)
            right = self._solve(exp.right, expressions)
            return operators[exp.operator](left, right)

        return int(exp)

    def _route_to_human(self, current: str = "root") -> list[str]:
        """Itemise the route between root and humn.

        Args:
            current (str): the current node

        Returns:
            list[str]: the results
        """
        exp = self.input[current]
        if current == "humn":
            return ["humn"]
        if isinstance(exp, Expression):
            left = self._route_to_human(exp.left)
            right = self._route_to_human(exp.right)
            return [current] + (left if "humn" in left else right)
        return []


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
