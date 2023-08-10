"""Solves the puzzle for Day 19 of Advent of Code 2017.

A Series of Tubes

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/19
"""
from collections.abc import Callable
from pathlib import Path
from string import ascii_uppercase
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 19
    TITLE = "A Series of Tubes"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[\|\-\+ A-Z]", str_processor)
        self.route = ""
        self.steps = -1

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        if self.route == "":
            self._solve()
        return self.route

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if self.steps == -1:
            self._solve()
        return self.steps

    def _solve(self) -> None:
        """Solve the route."""
        moves: dict[str, Callable[[int, int], tuple[int, int]]] = {
            UP: lambda a, b: (a, b - 1),
            DOWN: lambda a, b: (a, b + 1),
            LEFT: lambda a, b: (a - 1, b),
            RIGHT: lambda a, b: (a + 1, b),
        }
        direction = DOWN

        x, y = next(k for k, v in self.input.items() if k[1] == 0 and v == "|")

        self.route = ""
        self.steps = 0

        while True:
            c = self.input[(x, y)]
            if c == " ":
                break

            self.steps += 1

            if c in ascii_uppercase:
                self.route += c

            if c == "+":
                if direction in [UP, DOWN]:
                    if self.input[moves[RIGHT](x, y)] == "-":
                        direction = RIGHT
                    else:
                        direction = LEFT
                elif self.input[moves[UP](x, y)] == "|":
                    direction = UP
                else:
                    direction = DOWN

            x, y = moves[direction](x, y)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
