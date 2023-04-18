"""Solves the puzzle for Day 18 of Advent of Code 2020.

Operation Order

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/18
"""
from operator import add, mul
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 18
    TITLE = "Operation Order"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[ +*()0-9]+", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self._calc(line, addition_first=False) for line in self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self._calc(line, addition_first=True) for line in self.input)

    def _calc(self, expression: str, addition_first: bool) -> int:
        """Calculate the expression, recursively.

        Args:
            expression (str): the expression string
            addition_first (bool): multiplication precedence

        Returns:
            int: the result
        """
        if "(" in expression:
            # evaluate the bracketted expression, then call calc again
            start = expression.index("(")
            end = len(expression)
            level = 0
            for i in range(start, len(expression)):
                if expression[i] == "(":
                    level += 1
                elif expression[i] == ")":
                    level -= 1
                if level == 0:
                    end = i
                    break
            return self._calc(
                expression[0:start]
                + str(self._calc(expression[start + 1 : end], addition_first))
                + expression[end + 1 :],
                addition_first,
            )
        else:
            tokens = expression.split(" ")
            if addition_first:
                while "+" in tokens:
                    i = tokens.index("+")
                    x = int(tokens[i - 1]) + int(tokens[i + 1])
                    tokens = tokens[: i - 1] + [str(x)] + tokens[i + 2 :]

            x = int(tokens[0])
            for op, n in zip(tokens[1::2], tokens[2::2]):
                f = add if op == "+" else mul
                x = f(x, int(n))
            return x


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
