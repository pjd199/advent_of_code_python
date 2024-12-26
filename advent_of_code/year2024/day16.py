"""Solves the puzzle for Day 16 of Advent of Code 2024.

Reindeer Maze

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/16
"""

from collections import deque
from heapq import heapify, heappop, heappush
from sys import maxsize

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 16
    TITLE = "Reindeer Maze"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[.#SE]+", str_processor)
        self.cache: tuple[int, int] | None = None

    def _solve(self) -> tuple[int, int]:
        """Solve part two of the puzzle.

        Returns:
            tuple[int, int]: least cost, length of sspectators route
        """
        if self.cache:
            return self.cache

        # find the start and end
        start = next((x, y) for (x, y), v in self.input.items() if v == "S")
        end = next((x, y) for (x, y), v in self.input.items() if v == "E")
        direction = 0

        # initialise Dykstra's shortest path alogrithm
        priority_queue = [
            (maxsize, d, x, y)
            for (x, y), v in self.input.items()
            for d in range(4)
            if v in ".SE"
        ]
        heapify(priority_queue)
        heappush(priority_queue, (0, 0, *start))
        costs = {(x, y, d): c for c, d, x, y in priority_queue} | {start: 0}
        trace = {}

        while priority_queue:
            cost, direction, x, y = heappop(priority_queue)
            if cost > costs[(x, y, direction)]:
                continue

            # next nodes
            moves = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
            routes = (
                (moves[direction], 1, direction),
                *(((x, y), 1000, (direction + turn) % len(moves)) for turn in [-1, 1]),
            )
            # check for lowest cost paths
            for position, cost_to_neighbour, new_direction in routes:
                tentative = cost + cost_to_neighbour
                if (*position, new_direction) in costs:
                    if tentative < costs[(*position, new_direction)]:
                        costs[(*position, new_direction)] = tentative
                        trace[(*position, new_direction)] = {(x, y, direction)}
                        heappush(
                            priority_queue,
                            (tentative, new_direction, *position),
                        )
                    elif tentative == costs[(*position, new_direction)]:
                        trace[(*position, new_direction)].add((x, y, direction))

        # calculate the spectators route
        end_direction = min((costs[(*end, d)], d) for d in range(4))[1]
        stack = deque([*trace[(*end, end_direction)]])
        spectators = {start, end}
        while stack:
            x, y, d = stack.pop()
            if (x, y) == start:
                continue
            spectators.add((x, y))
            stack.extend([*trace[(x, y, d)]])

        self.cache = (costs[(*end, end_direction)], len(spectators))
        return self.cache

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        costs, _ = self._solve()
        return costs

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        _, spectators = self._solve()
        return spectators


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
