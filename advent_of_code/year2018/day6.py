"""Solves the puzzle for Day 6 of Advent of Code 2018.

Chronal Coordinates

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/6
"""
from collections import Counter
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
    DAY = 6
    TITLE = "Chronal Coordinates"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"(?P<x>\d+), (?P<y>\d+)", int_tuple_processor)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # find the min and max point
        min_x = min(x for x, _ in self.input)
        max_x = max(x for x, _ in self.input)
        min_y = min(y for _, y in self.input)
        max_y = max(y for _, y in self.input)

        # find the areas
        grid = {}
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                dist = [
                    (abs(input_x - x) + abs(input_y - y), i)
                    for i, (input_x, input_y) in enumerate(self.input)
                ]
                dist.sort(key=lambda x: x[0])

                if dist[0][0] != dist[1][0]:
                    grid[(x, y)] = dist[0][1]

        # find the infinite groups
        edges = (
            {(x, min_y) for x in range(min_x, max_x + 1)}
            | {(x, max_y) for x in range(min_x, max_x + 1)}
            | {(min_x, y) for y in range(min_y, max_y + 1)}
            | {(max_x, y) for y in range(min_y, max_y + 1)}
        )
        infinite = {group for point, group in grid.items() if point in edges}

        # find the answer
        return Counter(
            filter(lambda group: group not in infinite, grid.values())
        ).most_common(1)[0][1]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # find the min and max point
        min_x = min(x for x, _ in self.input)
        max_x = max(x for x, _ in self.input)
        min_y = min(y for _, y in self.input)
        max_y = max(y for _, y in self.input)

        # find the area
        size = 0
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                total = sum(
                    abs(input_x - x) + abs(input_y - y)
                    for i, (input_x, input_y) in enumerate(self.input)
                )
                if total < 10000:
                    size += 1

        return size


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
