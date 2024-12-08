"""Solves the puzzle for Day 8 of Advent of Code 2024.

Resonant Collinearity

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/8
"""

from itertools import count, permutations

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 8
    TITLE = "Resonant Collinearity"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[a-zA-Z0-9.]", str_processor)

    def _solve(self, resonance: bool) -> int:
        """Solve the puzzle.

        Args:
            resonance (bool): True for resonance mode (part two)

        Returns:
            int: the number of antinodes in the grid
        """
        (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*self.input))

        frequencies: dict[str, set[tuple[int, int]]] = {}
        for location, symbol in self.input.items():
            if symbol != ".":
                frequencies.setdefault(symbol, set()).add(location)

        antinodes: set[tuple[int, int]] = set()
        for locations in frequencies.values():
            for (x1, y1), (x2, y2) in permutations(locations, r=2):
                dx, dy = x2 - x1, y2 - y1
                iterable = count() if resonance else iter([1])
                for i in iterable:
                    if min_x <= x2 + i * dx <= max_x and min_y <= y2 + i * dy <= max_y:
                        antinodes.add((x2 + i * dx, y2 + i * dy))
                    else:
                        break
        return len(antinodes)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(resonance=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(resonance=True)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
