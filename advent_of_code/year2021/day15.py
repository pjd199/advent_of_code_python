"""Solves the puzzle for Day 15 of Advent of Code 2021.

Chiton

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/15
"""
from copy import deepcopy
from heapq import heapify, heappop, heappush
from pathlib import Path
from sys import maxsize, path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 15
    TITLE = "Chiton"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"\d", int_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._dykstra_distance(self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        grid = deepcopy(self.input)
        grid.extend(
            [
                [x + i if (x + i) <= 9 else ((x + i) % 10) + 1 for x in row]
                for i in range(1, 5)
                for row in self.input
            ]
        )
        for row in grid:
            row.extend(
                [
                    x + i if (x + i) <= 9 else ((x + i) % 10) + 1
                    for i in range(1, 5)
                    for x in row
                ]
            )
        return self._dykstra_distance(grid)

    def _dykstra_distance(self, grid: list[list[int]]) -> int:
        """Use Dykstra's Algorithm to find the distances source and last node.

        Args:
            grid (list[list[int]]): the input grid

        Returns:
            int: the distances to the final node
        """
        priority_queue = [
            (maxsize, (x, y))
            for y in range(len(grid))
            for x in range(len(grid[y]))
            if (x, y) != (0, 0)
        ]
        heapify(priority_queue)
        heappush(priority_queue, (0, (0, 0)))
        distances = {x[1]: x[0] for x in priority_queue}
        visited = set()

        while priority_queue:
            distance, (x, y) = heappop(priority_queue)
            if distance > distances[(x, y)]:
                continue

            routes = [
                ((x1, y1), grid[y1][x1])
                for x1, y1 in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
                if 0 <= y1 < len(grid)
                and 0 <= x1 < len(grid[y1])
                and (x1, y1) not in visited
            ]

            for position, distance_to_neighbour in routes:
                tentative_distance = distance + distance_to_neighbour
                if tentative_distance < distances[position]:
                    distances[position] = tentative_distance
                    heappush(priority_queue, (tentative_distance, position))
            visited.add((x, y))

        return distances[(len(grid) - 1, len(grid) - 1)]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
