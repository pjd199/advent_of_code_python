"""Solves the puzzle for Day 18 of Advent of Code 2022.

Boiling Boulders

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/18
"""
from collections import deque
from pathlib import Path
from sys import path
from typing import Deque, List, Tuple

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

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
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
        min_x = min(x for x, _, _ in self.input) - 1
        max_x = max(x for x, _, _ in self.input) + 1
        min_y = min(y for _, y, _ in self.input) - 1
        max_y = max(y for _, y, _ in self.input) + 1
        min_z = min(z for _, _, z in self.input) - 1
        max_z = min(z for _, _, z in self.input) + 1

        queue: Deque[Tuple[int, int, int]] = deque([(0, 0, 0)])
        water = set()

        while queue:
            x, y, z = queue.popleft()

            for x1, y1, z1 in self._adjacent(x, y, z):
                if (
                    (x1, y1, z1) not in water
                    and (x1, y1, z1) not in self.input
                    and min_x <= x1 <= max_x
                    and min_y <= y1 <= max_y
                    and min_z <= z1 <= max_z
                ):
                    queue.append((x1, y1, z1))
                    water.add((x1, y1, z1))

        return sum(
            1
            for x, y, z in self.input
            for x1, y1, z1 in self._adjacent(x, y, z)
            if (x1, y1, z1) in water
        )

    def _adjacent(self, x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
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
