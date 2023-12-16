"""Solves the puzzle for Day 11 of Advent of Code 2023.

Cosmic Expansion

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/11
"""
from itertools import combinations
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 11
    TITLE = "Cosmic Expansion"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"[.#]", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self.expand_universe(2)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self.expand_universe(1000000)

    def expand_universe(self, expansion: int) -> int:
        """Expand the universe.

        Args:
            expansion (int): expansion factor

        Returns:
            int: _description_
        """
        y_factors = [1 if "#" in row else expansion for row in self.input]
        x_factors = [
            1
            if "#" in (self.input[x][i] for x in range(len(self.input)))
            else expansion
            for i in range(len(self.input[0]))
        ]
        galaxies = [
            (x, y)
            for y in range(len(self.input))
            for x in range(len(self.input[y]))
            if self.input[y][x] == "#"
        ]
        return sum(
            sum(x_factors[min(x1, x2) : max(x1, x2)])
            + sum(y_factors[min(y1, y2) : max(y1, y2)])
            for (x1, y1), (x2, y2) in combinations(galaxies, 2)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
