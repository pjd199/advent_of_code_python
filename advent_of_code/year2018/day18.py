"""Solves the puzzle for Day 18 of Advent of Code 2018.

Settlers of The North Pole

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/18
"""
from copy import deepcopy
from itertools import chain
from pathlib import Path
from sys import maxsize, path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 18
    TITLE = "Settlers of The North Pole"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"[\.#|]", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(10)[-1]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        target = 1000000000

        # solve enough cycles to establish the repeating pattern
        values = self._solve(target, break_after_duplicates=100)

        # find the period of the repeating pattern
        period = 1
        while values[-1] != values[-1 - period]:
            period += 1

        # extract the repeating pattern
        pattern = values[-period:]

        # calculate the answer for target
        return pattern[(target - len(values) - 1) % len(pattern)]

    def _solve(self, length: int, break_after_duplicates: int = maxsize) -> List[int]:
        """Solve the puzzle.

        Args:
            length (int): number of times to repeat
            break_after_duplicates (int): find this many duplicates, then return

        Returns:
            List[int]: the resouce value of each iteration
        """
        grid = deepcopy(self.input)
        values = []

        for _ in range(length):
            new_grid = []

            for y, row in enumerate(grid):
                new_row = []
                for x, state in enumerate(row):
                    adjacent = [
                        (x - 1, y - 1),
                        (x, y - 1),
                        (x + 1, y - 1),
                        (x - 1, y),
                        (x + 1, y),
                        (x - 1, y + 1),
                        (x, y + 1),
                        (x + 1, y + 1),
                    ]
                    adjacent_squares = [
                        grid[y1][x1]
                        for x1, y1 in adjacent
                        if 0 <= x1 < len(row) and 0 <= y1 < len(grid)
                    ]
                    adjacent_trees = adjacent_squares.count("|")
                    adjacent_lumberyards = adjacent_squares.count("#")

                    if state == "." and adjacent_trees >= 3:
                        # open -> tree
                        new_row.append("|")

                    elif (state == "|" and adjacent_lumberyards >= 3) or (
                        state == "#"
                        and adjacent_trees >= 1
                        and adjacent_lumberyards >= 1
                    ):
                        # open or lumberyard -> lumberyard
                        new_row.append("#")

                    elif state == "#":
                        # lumberyard -> open
                        new_row.append(".")

                    else:
                        # no change
                        new_row.append(state)
                new_grid.append(new_row)

            # save the new_grid for the next round
            grid = new_grid

            # store the resource value
            grid_values = list(chain.from_iterable(grid))
            values.append(grid_values.count("|") * grid_values.count("#"))

            if (len(set(values)) + break_after_duplicates) < len(values):
                break

        return values


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
