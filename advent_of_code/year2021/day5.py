"""Solves the puzzle for Day 5 of Advent of Code 2021.

Hydrothermal Venture

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/5
"""
from collections import Counter
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 5
    TITLE = "Hydrothermal Venture"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"(\d+),(\d+) -> (\d+),(\d+)", int_tuple_processor)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(all_paths=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(all_paths=True)

    def _solve(self, all_paths: bool) -> int:
        """Solve the puzzle.

        Args:
            all_paths (bool): if True, include diagonal paths

        Returns:
            int: the result
        """
        counter: Counter[tuple[int, int]] = Counter()
        for x1, y1, x2, y2 in self.input:
            if x1 == x2:
                counter.update((x1, y) for y in range(min(y1, y2), max(y1, y2) + 1))
            elif y1 == y2:
                counter.update((x, y1) for x in range(min(x1, x2), max(x1, x2) + 1))
            elif all_paths:
                counter.update(
                    zip(
                        range(x1, x2 + (1 if x2 > x1 else -1), 1 if x2 > x1 else -1),
                        range(y1, y2 + (1 if y2 > y1 else -1), 1 if y2 > y1 else -1),
                    )
                )
        return sum(1 for v in counter.values() if v > 1)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
