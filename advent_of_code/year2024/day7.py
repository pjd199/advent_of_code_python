"""Solves the puzzle for Day 7 of Advent of Code 2024.

Bridge Repair

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/7
"""

from collections.abc import Sequence
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 7
    TITLE = "Bridge Repair"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input, (r"\d+", int_processor), delimiter=r"[: ]+"
        )

    def _solve(self, concat: bool) -> int:
        """Solve the puzzle.

        Args:
            concat (bool): if True, allow concat operator

        Returns:
            int: the result
        """

        def valid(target: int, terms: Sequence[int]) -> bool:
            if len(terms) == 1:
                return target == terms[0]

            *rest, tail = terms
            if tail < target and valid(target - tail, rest):
                return True
            if target % tail == 0 and valid(target // tail, rest):
                return True
            return (
                concat
                and len(str(tail)) < len(str(target))
                and str(target).endswith(str(tail))
                and valid(int(str(target).removesuffix(str(tail))), rest)
            )

        return sum(target for target, *terms in self.input if valid(target, terms))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(concat=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(concat=True)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
