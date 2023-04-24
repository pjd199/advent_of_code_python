"""Solves the puzzle for Day 17 of Advent of Code 2021.

Trick Shot

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/17
"""
from pathlib import Path
from sys import maxsize, path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 17
    TITLE = "Trick Shot"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.min_x, self.max_x, self.min_y, self.max_y = parse_single_line(
            puzzle_input,
            r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)",
            int_tuple_processor,
        )
        self.hits: dict[tuple[int, int], int] = {}

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._solve()
        return max(self.hits.values())

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._solve()
        return len(self.hits)

    def _solve(self) -> None:
        """Solve the puzzle."""
        if self.hits:
            return

        for vel_y in range(self.min_y, 100):
            for vel_x in range(self.max_x + 1):
                x, y, vx, vy = 0, 0, vel_x, vel_y
                apex = -maxsize
                while (y + vy) >= self.min_y and (x + vx) <= self.max_x:
                    x += vx
                    y += vy
                    vx += 0 if vx == 0 else (1 if vx < 0 else -1)
                    vy -= 1
                    apex = max(apex, y)
                if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y:
                    # on target!!!
                    self.hits[(vel_x, vel_y)] = apex


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
