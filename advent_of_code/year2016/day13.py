"""Solves the puzzle for Day 13 of Advent of Code 2016.

A Maze of Twisty Little Cubicles
For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/13
"""
from collections import deque
from collections.abc import Callable
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 13
    TITLE = "A Maze of Twisty Little Cubicles"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.number = parse_single_line(puzzle_input, r"\d+", int_processor)
        self.has_run = False

    def _open_space(self, x: int, y: int) -> bool:
        """Check to see if this location is open space.

        Args:
            x (int): x co-ordinate
            y (int): y co-ordinate

        Returns:
            bool: True is open space, else False
        """
        value = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + self.number
        return sum([1 for c in f"{value:b}" if c == "1"]) % 2 == 0

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return self.steps_to_target

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return self.within_50_steps

    def _run(self) -> None:
        """Run the simulation, using a breadth first search algorithm."""
        if self.has_run:
            return
        self.has_run = True

        moves: list[Callable[[int, int], tuple[int, int]]] = [
            lambda x, y: (x, y - 1),
            lambda x, y: (x + 1, y),
            lambda x, y: (x, y + 1),
            lambda x, y: (x - 1, y),
        ]

        queue: deque[tuple[int, int, int]] = deque([(1, 1, 0)])
        visited: set[tuple[int, int]] = {(1, 1)}

        self.within_50_steps = 0
        self.steps_to_target = 0
        while queue:
            x, y, steps = queue.popleft()

            if (x, y) == (31, 39):
                self.steps_to_target = steps
                break

            if steps <= 50:
                self.within_50_steps += 1

            for move in moves:
                x1, y1 = move(x, y)
                if x1 >= 0 and y1 >= 0 and (x1, y1) not in visited:
                    visited.add((x1, y1))
                    if self._open_space(x1, y1):
                        queue.append((x1, y1, steps + 1))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
