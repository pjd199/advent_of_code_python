"""Solves the puzzle for Day 24 of Advent of Code 2019.

Planet of Discord

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/24
"""
from collections import Counter
from itertools import chain, product
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 24
    TITLE = "Planet of Discord"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[.#]", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        bugs = frozenset((x, y) for (x, y), v in self.input.items() if v == "#")
        history = set()

        while bugs not in history:
            history.add(bugs)
            count = Counter(
                chain.from_iterable(self._adjacent2d(x, y) for (x, y) in bugs)
            )
            bugs = frozenset(
                (x, y)
                for (x, y) in count.keys() | bugs
                if ((x, y) in bugs and count[(x, y)] == 1)
                or ((x, y) not in bugs and count[(x, y)] in [1, 2])
            )

        return sum(
            2**i
            for i, (y, x) in enumerate(product(range(5), range(5)))
            if (x, y) in bugs
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        bugs = frozenset((x, y, 0) for (x, y), v in self.input.items() if v == "#")

        for _ in range(200):
            count = Counter(
                chain.from_iterable(self._adjacent3d(x, y, z) for (x, y, z) in bugs)
            )
            bugs = frozenset(
                (x, y, z)
                for (x, y, z) in count.keys() | bugs
                if ((x, y, z) in bugs and count[(x, y, z)] == 1)
                or ((x, y, z) not in bugs and count[(x, y, z)] in [1, 2])
            )
        return len(bugs)

    def _adjacent2d(self, x: int, y: int) -> set[tuple[int, int]]:
        """Find cells adjacent to (x,y).

        Args:
            x (int): x co-ordinate
            y (int): y co-ordinate

        Returns:
            set[tuple[int, int]]: adjacent cells
        """
        return {
            (x1, y1)
            for x1, y1 in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
            if 0 <= x1 < 5 and 0 <= y1 < 5
        }

    def _adjacent3d(self, x: int, y: int, z: int) -> set[tuple[int, int, int]]:
        """Find cells adjacent to (x,y,z).

        Args:
            x (int): x co-ordinate
            y (int): y co-ordinate
            z (int): z co-ordinate

        Returns:
            set[tuple[int, int, int]]: adjacent cells
        """
        # locations on the same z
        adjacent = {
            (x1, y1, z)
            for x1, y1 in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
            if 0 <= x1 < 5 and 0 <= y1 < 5 and (x1, y1) != (2, 2)
        }
        # locations up a level (inside)
        if (x, y) == (2, 1):
            adjacent.update((x1, 0, z + 1) for x1 in range(5))
        elif (x, y) == (1, 2):
            adjacent.update((0, y1, z + 1) for y1 in range(5))
        elif (x, y) == (3, 2):
            adjacent.update((4, y1, z + 1) for y1 in range(5))
        elif (x, y) == (2, 3):
            adjacent.update((x1, 4, z + 1) for x1 in range(5))

        # locations down a level (outside)
        if y == 0:
            adjacent.add((2, 1, z - 1))
        elif y == 4:
            adjacent.add((2, 3, z - 1))

        if x == 0:
            adjacent.add((1, 2, z - 1))
        elif x == 4:
            adjacent.add((3, 2, z - 1))
        return adjacent


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
