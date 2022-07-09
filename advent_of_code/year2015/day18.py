"""Solution for day 18 of Advent of Code 2015."""
from copy import deepcopy
from typing import Dict, List, Tuple

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        self.input = {}
        for y, line in enumerate(puzzle_input):
            for x, light in enumerate(line):
                if light == "#" or light == ".":
                    self.input[(x, y)] = light
                else:
                    raise RuntimeError(f"Parse error on line {y + 1}: {line}")

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
