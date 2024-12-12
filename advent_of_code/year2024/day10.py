"""Solves the puzzle for Day 10 of Advent of Code 2024.

Hoof It

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/10
"""

from collections import deque

from advent_of_code.utils.parser import int_processor, parse_grid
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 10
    TITLE = "Hoof It"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"\d", int_processor)

    def _solve(self) -> tuple[int, int]:
        """Rate the trail starting at (x, y).

        Returns:
            tuple[int, int]: (number of peaks, number of routes)
        """
        trailheads = [(x, y) for (x, y), z in self.input.items() if z == 0]
        peaks_count = 0
        routes_count = 0

        for start_x, start_y in trailheads:
            queue = deque([(start_x, start_y)])
            peaks = set()
            routes = 0

            while queue:
                x, y = queue.popleft()

                if self.input[(x, y)] == 9:
                    peaks.add((x, y))
                    routes += 1
                    continue

                moves = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
                for move in moves:
                    if (
                        move in self.input
                        and self.input[move] - 1 == self.input[(x, y)]
                    ):
                        queue.append(move)
            peaks_count += len(peaks)
            routes_count += routes
        return peaks_count, routes_count

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        peaks, _ = self._solve()
        return peaks

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        _, routes = self._solve()
        return routes


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
