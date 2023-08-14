"""Solves the puzzle for Day 3 of Advent of Code 2015.

Perfectly Spherical Houses in a Vacuum

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/3
"""
from dataclasses import dataclass
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass(eq=True, frozen=True)
class _Point:
    x: int
    y: int


class Solver(SolverInterface):
    """Solver for day 3 of Advent of Code 2015."""

    YEAR = 2015
    DAY = 3
    TITLE = "Perfectly Spherical Houses in a Vacuum"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        mapping = {
            "^": _Point(0, 1),
            ">": _Point(1, 0),
            "v": _Point(0, -1),
            "<": _Point(-1, 0),
        }
        self.input = parse_tokens_single_line(
            puzzle_input, (r"[\^>v<]", lambda m: mapping[m[0]])
        )

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # move santa around the world based on the directions provided,
        # recording the unique houses using a set
        santa = _Point(0, 0)
        houses = {santa}
        for direction in self.input:
            santa = _Point(santa.x + direction.x, santa.y + direction.y)
            houses.add(santa)
        return len(houses)

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # santa is index 0, robot santa is index 1
        # move santa and robot santa around the world based on the
        # directions provided, recording the unique houses using a set
        avatar = [_Point(0, 0), _Point(0, 0)]
        houses = {_Point(0, 0)}

        for i, direction in enumerate(self.input):
            avatar[i % 2] = _Point(
                avatar[i % 2].x + direction.x, avatar[i % 2].y + direction.y
            )
            houses.add(avatar[i % 2])
        return len(houses)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
