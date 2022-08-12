"""Solution for day 10 of Advent of Code 2015."""
from itertools import groupby
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 10
    TITLE = "Elves Look, Elves Say"

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

        if len(puzzle_input) != 1 or not puzzle_input[0].isnumeric():
            raise RuntimeError(
                f"Puzzle input should be sequence of "
                f"numbers, found: {puzzle_input[0]}"
            )

        self.puzzle_input = puzzle_input[0]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        seq = self.puzzle_input
        for _ in range(40):
            seq = "".join(str(len(list(g))) + k for k, g in groupby(seq))
        return len(seq)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        seq = self.puzzle_input
        for _ in range(50):
            seq = "".join(str(len(list(g))) + k for k, g in groupby(seq))
        return len(seq)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
