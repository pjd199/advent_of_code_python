"""Solution for day 2 of Advent of Code 2015."""
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 2
    TITLE = "I Was Told There Would Be No Math"

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

        self.input = []
        pattern = compile(r"(?P<L>[0-9]+)x(?P<W>[0-9]+)x(?P<H>[0-9]+)")
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                # add the dimensions of the cuboid, sorted by smallest first
                self.input.append(
                    sorted([int(match["L"]), int(match["W"]), int(match["H"])])
                )
            else:
                raise RuntimeError(f"Invalid input on line {i + 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # cacluate the ammount of wrapping paper, as the sum of the
        # total area of the six sides of each cuboid,
        # plus the area of the smallest side of each cuboid
        # (dimensions are sorted during parsing in __init__)
        return sum([(3 * a * b) + (2 * b * c) + (2 * c * a) for a, b, c in self.input])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # calculate the ammount of ribbon, as the sum of the perimiter
        # of the smallest face, plus the volume
        return sum([2 * (a + b) + (a * b * c) for a, b, c in self.input])


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
