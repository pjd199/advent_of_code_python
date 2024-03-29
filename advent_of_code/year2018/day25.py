"""Solves the puzzle for Day 25 of Advent of Code 2018.

Four-Dimensional Adventure

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/25
"""
from collections import deque
from pathlib import Path
from sys import path
from typing import NoReturn

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 25
    TITLE = "Four-Dimensional Adventure"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"(-?\d+),(-?\d+),(-?\d+),(-?\d+)", int_tuple_processor)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # use a breadth first search to group the closest points together
        available = set(self.input)
        constellations: list[set[tuple[int, ...]]] = []
        queue: deque[tuple[int, ...]] = deque([])

        while available:
            constellation: set[tuple[int, ...]] = set()
            constellations.append(constellation)
            queue.append(available.pop())
            while queue:
                point = queue.popleft()
                constellation.add(point)
                points = {
                    x
                    for x in available
                    if sum(abs(i - j) for i, j in zip(x, point)) <= 3
                }
                available -= points
                queue.extend(points)

        return len(constellations)

    def solve_part_two(self) -> NoReturn:
        """Solve part two of the puzzle.

        Returns:
            NoReturn: This will never return normally

        Raises:
            NotImplementedError: always!
        """
        raise NotImplementedError


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
