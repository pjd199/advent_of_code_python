"""Solves the puzzle for Day 18 of Advent of Code 2024.

RAM Run

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/18
"""

from heapq import heapify, heappop, heappush
from sys import maxsize

from advent_of_code.utils.parser import int_sequence_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 18
    TITLE = "RAM Run"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = list(
            map(
                tuple,
                parse_lines(puzzle_input, (r"(\d+),(\d+)", int_sequence_processor)),
            )
        )

    def _shortest_path(self, limit: int) -> int:
        """Find the shortest path.

        Args:
            limit (int): the time limit

        Returns:
            int: the shortest path
        """
        (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*self.input))
        start = (min_x, min_y)
        end = (max_x, max_y)
        blocked = set(self.input[:limit])
        safe = {
            (x, y)
            for x in range(min_x, max_x + 1)
            for y in range(min_y, max_y + 1)
            if (x, y) not in blocked
        }

        # initialise Dykstra's shortest path alogrithm
        costs: dict[tuple[int, int], int] = {(x, y): maxsize for x, y in safe} | {
            start: 0
        }
        priority_queue = [(c, x, y) for (x, y), c in costs.items()]
        heapify(priority_queue)

        while priority_queue:
            cost, x, y = heappop(priority_queue)
            if cost > costs[(x, y)]:
                continue

            # next nodes
            moves = (
                (mx, my)
                for mx, my in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
                if (mx, my) in safe
            )
            # check for lowest cost paths
            for position in moves:
                tentative = cost + 1
                if position in costs and tentative < costs[position]:
                    costs[position] = tentative
                    heappush(
                        priority_queue,
                        (tentative, *position),
                    )
        return costs[end]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._shortest_path(1024)

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        # binary search for the answer
        lower, upper = 0, len(self.input)
        while upper - lower > 1:
            middle = lower + (upper - lower) // 2
            if self._shortest_path(middle) < maxsize:
                lower = middle
            else:
                upper = middle

        return ",".join(map(str, self.input[lower]))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
