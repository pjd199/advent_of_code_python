"""Solves the puzzle for Day 14 of Advent of Code 2017.

Disk Defragmentation

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/14
"""
from collections import deque
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2017.knot_hash import knot_hash


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 14
    TITLE = "Disk Defragmentation"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"\w+", str_processor)
        self.grid: set[tuple[int, int]] = set()

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.grid:
            self._initialise_grid()

        return len(self.grid)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.grid:
            self._initialise_grid()

        total = 0
        search = set(self.grid)
        found = set()

        while search:
            group = self._find_group(*search.pop())
            search.difference_update(group)
            found.update(group)
            total += 1

        return total

    def _initialise_grid(self) -> None:
        """Initialise the grid."""
        self.grid = {
            (x, y)
            for y in range(128)
            for x, bit in enumerate(f"{int(knot_hash(f'{self.input}-{y}'), 16):0128b}")
            if bit == "1"
        }

    def _find_group(self, start_x: int, start_y: int) -> set[tuple[int, int]]:
        """Find a group of co-ordinates.

        Args:
            start_x (int): starting x co-ordinate
            start_y (int): starting y co-ordinate

        Returns:
            set[tuple[int, int]]: the found group
        """
        group = set()
        queue: deque[tuple[int, int]] = deque()
        queue.append((start_x, start_y))

        while queue:
            x, y = queue.popleft()
            group.add((x, y))
            for move in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
                if move in self.grid and move not in group:
                    queue.append(move)

        return group


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
