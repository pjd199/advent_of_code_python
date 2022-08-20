"""Solves the puzzle for Day 12 of Advent of Code 2015.

JSAbacusFramework.io

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/12
"""
from json import loads
from json.decoder import JSONDecodeError
from pathlib import Path
from sys import path
from typing import Any, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 12
    TITLE = "JSAbacusFramework.io"

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

        if len(puzzle_input) == 1:
            try:
                self.content = loads(puzzle_input[0])
            except JSONDecodeError:
                raise RuntimeError(f"Error parsing JSON, " f"found: {puzzle_input[0]}")
        else:
            raise RuntimeError(f"Error parsing JSON, " f"found: {puzzle_input[0]}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._content_sum(self.content, ignore_red=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        return self._content_sum(self.content, ignore_red=True)

    def _content_sum(self, obj: Any, ignore_red: bool) -> int:
        """Sum the content of obj.

        Resurcively add up all the number values in the arrays or dictionaries.
        If ignore_red is true, all dictionaries with a value "red" are ignored

        Args:
            obj (Any): object to sum
            ignore_red (bool): if True, ignore reds

        Returns:
            int: the sum
        """
        if isinstance(obj, int):
            return obj
        elif isinstance(obj, list):
            return sum([self._content_sum(x, ignore_red) for x in obj])
        elif isinstance(obj, dict) and (
            (not ignore_red) or ("red" not in obj.values())
        ):
            return sum([self._content_sum(x, ignore_red) for x in obj.values()])
        else:
            return 0


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
