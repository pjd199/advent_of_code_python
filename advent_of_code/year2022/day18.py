"""Solves the puzzle for Day 18 of Advent of Code 2022.

Boiling Boulders

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/18
"""
from collections import deque
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 18
    TITLE = "Boiling Boulders"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = set(
            parse_lines(puzzle_input, (r"(\d+),(\d+),(\d+)", int_tuple_processor))
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1
            for x, y, z in self.input
            for x1, y1, z1 in self._adjacent(x, y, z)
            if (x1, y1, z1) not in self.input
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # starting at (0,0,0), do a BFS to find all cubes that are water,
        # then find surface area by calculating edges rock touches water
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = (
            (min(a), max(a)) for a in zip(*self.input)
        )

        queue: deque[tuple[int, int, int]] = deque([(0, 0, 0)])
        water = set()

        while queue:
            x, y, z = queue.popleft()

            for x1, y1, z1 in self._adjacent(x, y, z):
                if (
                    (x1, y1, z1) not in water
                    and (x1, y1, z1) not in self.input
                    and min_x - 1 <= x1 <= max_x + 1
                    and min_y - 1 <= y1 <= max_y + 1
                    and min_z - 1 <= z1 <= max_z + 1
                ):
                    queue.append((x1, y1, z1))
                    water.add((x1, y1, z1))

        return sum(
            1
            for x, y, z in self.input
            for x1, y1, z1 in self._adjacent(x, y, z)
            if (x1, y1, z1) in water
        )

    def _adjacent(self, x: int, y: int, z: int) -> list[tuple[int, int, int]]:
        return [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
