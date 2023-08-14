"""Solves the puzzle for Day 22 of Advent of Code 2017.

Sporifica Virus

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/22
"""
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 22
    TITLE = "Sporifica Virus"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[.#]", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(
            10000,
            {
                "#": lambda direction: ((direction + 1) % 4, "."),  # turn right
                ".": lambda direction: ((direction - 1) % 4, "#"),  # turn left
            },
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(
            10000000,
            {
                ".": lambda direction: ((direction - 1) % 4, "W"),  # turn left
                "W": lambda direction: (direction, "#"),
                "#": lambda direction: ((direction + 1) % 4, "F"),  # turn right
                "F": lambda direction: ((direction + 2) % 4, "."),  # about turn
            },
        )

    def _solve(
        self, cycles: int, actions: dict[str, Callable[[int], tuple[int, str]]]
    ) -> int:
        """Run the simulation.

        Args:
            cycles (int): number of cycles fo run
            actions (dict[str, Callable[[int], tuple[int, str]]]): the action
                to perform on each cycle

        Returns:
            int: the number of infections
        """
        # copy the input grid
        grid = deepcopy(self.input)

        # setup the move functions
        moves: dict[int, Callable[[int, int], tuple[int, int]]] = {
            0: lambda x, y: (x, y - 1),  # up
            1: lambda x, y: (x + 1, y),  # left
            2: lambda x, y: (x, y + 1),  # down
            3: lambda x, y: (x - 1, y),  # right
        }
        direction = 0

        # place the current position in the centre of the grid (odd length sides)
        x, y = (
            max(x1 for x1, _ in grid) // 2,
            max(y1 for _, y1 in grid) // 2,
        )

        # run the simulation, counting the number of infections
        infections = 0
        for _ in range(cycles):
            direction, grid[(x, y)] = actions[grid.get((x, y), ".")](direction)
            if grid[(x, y)] == "#":
                infections += 1
            x, y = moves[direction](x, y)

        return infections


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
