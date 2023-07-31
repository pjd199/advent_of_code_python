"""Solves the puzzle for Day 24 of Advent of Code 2015.

It Hangs in the Balance

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/24
"""
from itertools import combinations
from math import prod
from pathlib import Path
from sys import path
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 24
    TITLE = "It Hangs in the Balance"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialsie the solver.

        Args:
            puzzle_input (List[str]): the input lines
        """
        self.presents = parse_lines(puzzle_input, (r"[0-9]+", int_processor))

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one.

        Returns:
            int: the result
        """
        return self._find(3)

    @cache_result
    def solve_part_two(self) -> int:
        """Solve two one.

        Returns:
            int: the result
        """
        return self._find(4)

    def _find(self, groups: int) -> int:
        """Find the product of the smallest group.

        Args:
            groups (int): the number of groups

        Returns:
            int: the product of the sum of the smallest group
        """
        target = sum(self.presents) // groups

        # split into groups
        result = []
        remainder = self.presents
        for _ in range(groups):
            group, remainder = self._split(remainder, target)
            result.append(group)
        return int(prod(result[0]))

    def _split(self, items: List[int], target: int) -> Tuple[List[int], List[int]]:
        """Split the item list into two groups, the first having the sum of target.

        Args:
            items (List[int]): the items to group
            target (int): the target sum of the group

        Returns:
            Tuple[List[int], List[int]]: returns a tuple with the found
                                        group then the remainer
        """
        result = []

        for x in range(1, len(items) + 1):
            group = sorted(
                [list(x) for x in combinations(items, x) if sum(list(x)) == target],
                key=prod,
            )
            if group:
                result = group[0]
                break

        return result, [x for x in items if x not in result]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
