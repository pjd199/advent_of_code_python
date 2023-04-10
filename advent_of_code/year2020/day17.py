"""Solves the puzzle for Day 17 of Advent of Code 2020.

Conway Cubes

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/17
"""
from itertools import product
from pathlib import Path
from sys import path
from typing import Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 17
    TITLE = "Conway Cubes"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[#.]", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(four_dimensional=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(four_dimensional=True)

    def _solve(self, four_dimensional: bool) -> int:
        """Solve the puzzle.

        Args:
            four_dimensional (bool): if true, run in 4D, else 3D

        Returns:
            int: the result
        """
        cycles = 6
        grid: Dict[Tuple[int, int, int, int], bool] = {
            (x, y, 0, 0): v == "#" for (x, y), v in self.input.items()
        }

        # for each cycle, create the next iteration of the grid
        for _ in range(cycles):
            # prepare the next grid
            next_grid: Dict[Tuple[int, int, int, int], bool] = {}
            # find the min and max values on each dimension
            (min_x, max_x), (min_y, max_y), (min_z, max_z), (min_w, max_w) = (
                (min(a), max(a)) for a in zip(*grid.keys())
            )

            # for each of the neighbouring squares
            for (x, y, z, w) in product(
                range(min_x - 1, max_x + 2),
                range(min_y - 1, max_y + 2),
                range(min_z - 1, max_z + 2),
                range(min_w - 1, max_w + 2) if four_dimensional else [0],
            ):
                # count the neighbours
                count = sum(
                    1
                    for (x1, y1, z1, w1) in product(
                        range(x - 1, x + 2),
                        range(y - 1, y + 2),
                        range(z - 1, z + 2),
                        range(w - 1, w + 2) if four_dimensional else [0],
                    )
                    if (x1, y1, z1, w1) in grid
                    and grid[(x1, y1, z1, w1)]
                    and (x, y, z, w) != (x1, y1, z1, w1)
                )
                # determine the status of the square in the next grid
                if (x, y, z, w) in grid and grid[(x, y, z, w)]:
                    next_grid[(x, y, z, w)] = count == 2 or count == 3
                else:
                    next_grid[(x, y, z, w)] = count == 3
            # move to the next grid
            grid = next_grid

        # return the number of active squares
        return sum(1 for active in grid.values() if active)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
