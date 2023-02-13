"""Solves the puzzle for Day 10 of Advent of Code 2019.

Monitoring Station

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/10
"""
from itertools import chain, groupby, zip_longest
from math import atan2, pi
from operator import itemgetter
from pathlib import Path
from sys import path
from typing import Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 10
    TITLE = "Monitoring Station"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = {
            k
            for k, v in parse_grid(puzzle_input, r"[.#]", str_processor).items()
            if v == "#"
        }
        self.location_found = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.location, visible = max(
            (
                ((x1, y1), (len({atan2(y2 - y1, x2 - x1) for x2, y2 in self.input})))
                for x1, y1 in self.input
            ),
            key=itemgetter(1),
        )
        self.location_found = True
        return visible

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.location_found:
            self.solve_part_one()
        x1, y1 = self.location

        # calculate the atan2 for each asteroid, then sort by angle and distance.
        # then group by angle and list the points
        asteroids: Dict[float, List[Tuple[int, int]]] = {
            angle: [point for _, point in points]
            for angle, points in groupby(
                sorted(
                    (
                        ((atan2(y2 - y1, x2 - x1) + (pi / 2)) % (2 * pi), (x2, y2))
                        for x2, y2 in self.input
                    ),
                    key=lambda a: (a[0], -(abs(x1 - a[1][0]) + abs(y1 - a[1][1]))),
                ),
                key=itemgetter(0),
            )
        }

        # vaporize the asteroids, which are now in an order, such that
        # we can take all the asteroids in first positions from the angle lists,
        # then all the second positions etc. Then select the 200th asteroid
        x, y = next(
            vaporized
            for i, vaporized in enumerate(
                filter(None, chain(*zip_longest(*asteroids.values())))
            )
            if i == 199
        )
        return (x * 100) + y


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
