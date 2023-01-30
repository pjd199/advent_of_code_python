"""Solves the puzzle for Day 23 of Advent of Code 2018.

Experimental Emergency Teleportation

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/23
"""
from math import ceil, log2
from operator import itemgetter
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 23
    TITLE = "Experimental Emergency Teleportation"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = {
            (x, y, z): r
            for x, y, z, r in parse_lines(
                puzzle_input,
                (r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", int_tuple_processor),
            )
        }

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        (x, y, z), radius = max(self.input.items(), key=itemgetter(1))

        return sum(
            1
            for x1, y1, z1 in self.input
            if abs(x - x1) + abs(y - y1) + abs(z - z1) <= radius
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # work out the bounding box as a cube, with sides of length a power of two
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = (
            (min(a), max(a)) for a in zip(*self.input)
        )
        side = 2 ** ceil(log2(max(max_x - min_x, max_y - min_y, max_z - min_z)))
        max_x = min_x + side
        max_y = min_y + side
        max_z = min_z + side

        (x, y, z) = (0, 0, 0)
        while side != 0:
            # break down the bounding box into smaller boxes,
            # and count how many nanobots are in range
            best = {
                (x, y, z): sum(
                    1
                    for (x1, y1, z1), r in self.input.items()
                    if abs(x - x1) + abs(y - y1) + abs(z - z1) <= r + side
                )
                for x in range(min_x, max_x + 1, side)
                for y in range(min_y, max_y + 1, side)
                for z in range(min_z, max_z + 1, side)
            }

            # centre the next bounding box around the best location,
            # then shrink the bounding box
            (x, y, z), _ = sorted(
                best.items(),
                key=lambda a: (-a[1], abs(a[0][0]) + abs(a[0][1]) + abs(a[0][2])),
            )[0]

            side //= 2
            (min_x, min_y, min_z) = (x - side, y - side, z - side)
            (max_x, max_y, max_z) = (x + side, y + side, z + side)

        return abs(x) + abs(y) + abs(z)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
