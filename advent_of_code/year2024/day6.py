"""Solves the puzzle for Day 6 of Advent of Code 2024.

Guard Gallivant

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/6
"""

from collections.abc import Sequence
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 6
    TITLE = "Guard Gallivant"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[.#>v<^]+", str_processor)

    def _simulate(
        self, grid: dict[tuple[int, int], str]
    ) -> tuple[Sequence[tuple[int, int]], bool]:
        """Simulate the gaurd's walk.

        Args:
            grid (dict[tuple[int, int], str]): the input grid

        Returns:
            tuple[Sequence[tuple[int, int]], bool]: (the route, loop detected)
        """
        directions = [">", "v", "<", "^"]
        moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        (x, y), symbol = next(
            (start, symbol) for start, symbol in self.input.items() if symbol in ">v<^"
        )
        direction = directions.index(symbol)
        visited: set[tuple[int, int, int]] = set()
        while (x, y) in grid and (x, y, direction) not in visited:
            visited.add((x, y, direction))
            dx, dy = moves[direction]
            if grid.get((x + dx, y + dy)) == "#":
                direction = (direction + 1) % 4
            else:
                x, y = x + dx, y + dy
        return [(x, y) for x, y, _ in visited], (x, y, direction) in visited

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        route, _ = self._simulate(self.input)
        return len(set(route))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        start = next(start for start, symbol in self.input.items() if symbol in ">v<^")
        original_route, _ = self._simulate(self.input)
        return sum(
            1
            for x, y in set(original_route) - {start}
            if self._simulate(self.input | {(x, y): "#"})[1]
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
