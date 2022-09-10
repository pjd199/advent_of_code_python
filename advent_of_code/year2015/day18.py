"""Solves the puzzle for Day 18 of Advent of Code 2015.

Like a GIF For Your Yard

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/18
"""
from copy import deepcopy
from pathlib import Path
from sys import path
from typing import Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 18
    TITLE = "Like a GIF For Your Yard"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        """
        self.input = parse_grid(puzzle_input, r"[#\.]", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        grid = deepcopy(self.input)
        for _ in range(100):
            grid.update({key: self._next_state(grid, *key) for key in grid})

        return len([x for x in grid.values() if x == "#"])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        grid = deepcopy(self.input)
        corners_stuck_on = {(0, 0): "#", (0, 99): "#", (99, 0): "#", (99, 99): "#"}
        for _ in range(100):
            grid.update(corners_stuck_on)
            grid.update({key: self._next_state(grid, *key) for key in grid})
        grid.update(corners_stuck_on)

        return len([x for x in grid.values() if x == "#"])

    def _next_state(self, grid: Dict[Tuple[int, int], str], x: int, y: int) -> str:
        """Calculate the next state of the light at position (x, y).

        Args:
            grid (Dict[Tuple[int, int], str]): the dictionary grid of lights
            x (int): x co-ordinate
            y (int): y co-ordinate

        Returns:
            str: the state, "#" for on, "." for off
        """
        neighbors = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]
        total_on = len([n for n in neighbors if grid.get(n, ".") == "#"])
        if grid[(x, y)] == "#":
            return "#" if (total_on == 2) or (total_on == 3) else "."
        else:
            return "#" if total_on == 3 else "."


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
