"""Solver for day 3 of Advent of Code 2015."""
from collections import namedtuple
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface

Point = namedtuple("Point", "x y")


class Solver(SolverInterface):
    """Solver for day 3 of Advent of Code 2015."""

    YEAR = 2015
    DAY = 3
    TITLE = "Perfectly Spherical Houses in a Vacuum"

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

        # translate input text into to direction Points
        input_map = {
            "^": Point(0, 1),
            ">": Point(1, 0),
            "v": Point(0, -1),
            "<": Point(-1, 0),
        }
        if not all([c in input_map for c in puzzle_input[0]]):
            raise RuntimeError(
                f"Puzzle input should only contain ^,>,v or < :"
                f"found {puzzle_input[0]}"
            )
        self.input = [input_map[c] for c in puzzle_input[0]]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # move santa around the world based on the directions provided,
        # recording the unique houses using a set
        santa = Point(0, 0)
        houses = {santa}
        for direction in self.input:
            santa = Point(santa.x + direction.x, santa.y + direction.y)
            houses.add(santa)
        return len(houses)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # santa is index 0, robot santa is index 1
        # move santa and robot santa around the world based on the
        # directions provided, recording the unique houses using a set
        avatar = [Point(0, 0), Point(0, 0)]
        houses = {Point(0, 0)}

        for i, direction in enumerate(self.input):
            avatar[i % 2] = Point(
                avatar[i % 2].x + direction.x, avatar[i % 2].y + direction.y
            )
            houses.add(avatar[i % 2])
        return len(houses)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
