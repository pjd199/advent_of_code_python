"""Solves the puzzle for Day 21 of Advent of Code 2017.

Fractal Art

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/21
"""
from itertools import chain
from pathlib import Path
from sys import path
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 21
    TITLE = "Fractal Art"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"([#/.]+) => ([#/.]+)", str_tuple_processor)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(5)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(18)

    def _solve(self, cycles: int) -> int:
        """Run the simulation.

        Args:
            cycles (int): number of cycles to complete

        Returns:
            int: the number of lights on (#) at the finish
        """

        def rotations(
            x: Tuple[Tuple[str, ...], ...]
        ) -> List[Tuple[Tuple[str, ...], ...]]:
            result = [x]
            for _ in range(3):
                x = tuple(zip(*x[::-1]))
                result.append(x)
            return result

        # starting grid
        grid = [list(".#."), list("..#"), list("###")]

        # build the rule book
        rules = {}
        for match, output in self.input:
            square = tuple(tuple(x) for x in match.split("/"))
            result = tuple(tuple(x) for x in output.split("/"))
            # add with no flip
            rules.update({r: result for r in rotations(square)})
            # add horizontal flip
            square = tuple(tuple(reversed(row)) for row in square)
            rules.update({r: result for r in rotations(square)})
            # add vertical flip
            square = tuple(reversed(square))
            rules.update({r: result for r in rotations(square)})
            # horizontal flip back for vertical + horizontal flip
            square = tuple(tuple(reversed(row)) for row in square)
            rules.update({r: result for r in rotations(square)})

        # run the iterations of the simulation
        for _ in range(cycles):
            width = 2 if len(grid) % 2 == 0 else 3
            new_grid: List[List[str]] = []
            for y in range(0, len(grid), width):
                new_grid += [[] for _ in range(width + 1)]
                for x in range(0, len(grid), width):
                    square = tuple(
                        tuple(grid[ty][x : x + width]) for ty in range(y, y + width)
                    )
                    replacement = rules[square]
                    for i, row in enumerate(replacement):
                        new_grid[(y * (width + 1) // width) + i] += list(row)
            grid = new_grid

        return sum(1 for x in chain.from_iterable(grid) if x == "#")


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
