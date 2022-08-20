"""Solves the puzzle for Day 18 of Advent of Code 2016.

Like a Rogue

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/18
"""
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 18
    TITLE = "Like a Rogue"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        pattern = compile(r"[\.\^]+")
        for i, line in enumerate(puzzle_input):
            if (m := pattern.fullmatch(line)) and (i == 0):
                self.input = m[0]
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i + 1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(40)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(400000)

    def _run(self, rows: int) -> int:
        """Run the simulation.

        Mapping the "^" to True, the 4 rules reduce reduce to left != right

        Args:
            rows (int): the number of rows

        Returns:
            int: the total number of safe / "." / False
        """
        traps = 0
        row = [x == "^" for x in self.input]
        for _ in range(rows):
            traps += row.count(True)
            row = [
                left != right for left, right in zip([False] + row, row[1:] + [False])
            ]
        return (len(row) * rows) - traps


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
