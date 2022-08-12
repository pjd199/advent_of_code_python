"""Solution for day 24 of Advent of Code 2015."""
from itertools import combinations
from math import prod
from pathlib import Path
from re import compile
from sys import path
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
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

        Raises:
            RuntimeError: raised when unable to parse
        """
        self.presents = []

        # validate and parse the input
        if puzzle_input is None or len(puzzle_input) == 0:
            raise RuntimeError("Puzzle input is empty")

        pattern = compile(r"^(?P<num>[0-9]+)$")
        for i, line in enumerate(puzzle_input):
            m = pattern.match(line)
            if m:
                self.presents.append(int(m.groupdict()["num"]))
            else:
                raise RuntimeError(f"Error parsing on line {i + 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one.

        Returns:
            int: the result
        """
        return self._find(3)

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
        return prod(result[0])

    def _split(self, items: List[int], target: int) -> Tuple[List[int], List[int]]:
        """Split the item list into two groups, the first of which has the sum of target.

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
