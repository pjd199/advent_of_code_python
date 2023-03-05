"""Solves the puzzle for Day 15 of Advent of Code 2019.

Oxygen System

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/15
"""
from collections import deque
from copy import deepcopy
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Deque, Dict, List, Optional, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


@unique
class GridValue(Enum):
    """Values for the grid."""

    wall = 0
    space = 1
    oxygen = 2


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 15
    TITLE = "Oxygen System"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.computer = IntcodeComputer(puzzle_input)
        self.grid: Dict[Tuple[int, int], GridValue] = {}

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.generate_grid()
        return self.navigate(start=(0, 0), finish=self.oxygen_system_location)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self.generate_grid()
        return self.navigate(start=self.oxygen_system_location, finish=None)

    def generate_grid(self) -> None:
        """Generate the grid."""
        if self.grid:
            return

        # use a breadth first search to create the grid
        x, y = (0, 0)
        queue: Deque[Tuple[int, int, int, IntcodeComputer]] = deque(
            [(x, y, 0, deepcopy(self.computer))]
        )
        self.grid = {(x, y): GridValue.space}

        while queue:
            x, y, steps, computer = queue.popleft()

            for x1, y1, command in self.next_moves(x, y):
                if (x1, y1) not in self.grid:
                    copied_computer = deepcopy(computer)
                    copied_computer.input_data(command)
                    copied_computer.execute(sleep_after_output=True)
                    self.grid[(x1, y1)] = GridValue(copied_computer.read_output())
                    if self.grid[(x1, y1)] == GridValue.space:
                        queue.append((x1, y1, steps + 1, copied_computer))

        # find the location of the oxygen system
        self.oxygen_system_location = next(
            (x, y) for (x, y), v in self.grid.items() if v == GridValue.oxygen
        )

    def next_moves(self, x: int, y: int) -> Tuple[Tuple[int, int, int], ...]:
        """Return an iterator for the moves from (x,y).

        Args:
            x (int): x co-ordinate
            y (int): y co-ordinate

        Returns:
            Iterator[Tuple[int, int, int]]: the moves
        """
        return (
            (x, y - 1, 1),
            (x, y + 1, 2),
            (x - 1, y, 3),
            (x + 1, y, 4),
        )

    def navigate(
        self, start: Tuple[int, int], finish: Optional[Tuple[int, int]]
    ) -> int:
        """Navigate the grid, from start to finish.

        Args:
            start (Tuple[int,int]): starting co-ordinates. Defaults to (0, 0).
            finish (Tuple[int,int]): finishing co-ordinates. Defaults to None.

        Returns:
            int: number of steps from start and finish
        """
        # create a set of co-ordinates to visit, and find target point
        grid = {(x, y) for (x, y), v in self.grid.items() if v != GridValue.wall}

        # perform a breadth first search to find the oxygen
        x, y = start
        queue: Deque[Tuple[int, int, int]] = deque([(x, y, 0)])
        visited = {(x, y)}
        steps = -1
        while queue:
            x, y, steps = queue.popleft()

            if (x, y) == finish:
                break

            for x1, y1, _ in self.next_moves(x, y):
                if (x1, y1) in grid and (x1, y1) not in visited:
                    visited.add((x1, y1))
                    queue.append((x1, y1, steps + 1))

        return steps


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
