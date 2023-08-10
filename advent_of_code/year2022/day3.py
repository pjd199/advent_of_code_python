"""Solves the puzzle for Day 3 of Advent of Code 2022.

Rucksack Reorganization

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/3
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 3
    TITLE = "Rucksack Reorganization"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[a-zA-Z]+", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._priorities(
            [
                list(set(x[: len(x) // 2]).intersection(set(x[len(x) // 2 :])))[0]
                for x in self.input
            ]
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._priorities(
            [
                list(
                    set(self.input[i])
                    .intersection(set(self.input[i + 1]))
                    .intersection(self.input[i + 2])
                )[0]
                for i in range(0, len(self.input), 3)
            ]
        )

    def _priorities(self, values: list[str]) -> int:
        return sum(
            (ord(x) - ord("A")) + 27 if x.isupper() else (ord(x) - ord("a")) + 1
            for x in values
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
