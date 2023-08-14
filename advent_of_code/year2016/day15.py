"""Solves the puzzle for Day 15 of Advent of Code 2016.

Timing is Everything

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/15
"""
from dataclasses import dataclass
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Disc:
    """Stores disc data."""

    positions: int
    start: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 15
    TITLE = "Timing is Everything"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.discs = parse_lines(
            puzzle_input,
            (
                r"Disc #(?P<number>\d+) has (?P<positions>\d+) positions; "
                r"at time=0, it is at position (?P<start>\d+).",
                dataclass_processor(Disc),
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(self.discs)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._run([*self.discs, Disc(11, 0)])

    def _run(self, discs: list[Disc]) -> int:
        """Run the simulation.

        Args:
            discs (list[Disc]): the input discs

        Returns:
            int: the result
        """
        time = 0
        while any(
            (
                ((disc.start + time + t + 1) % disc.positions) != 0
                for t, disc in enumerate(discs)
            )
        ):
            time += 1

        return time


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
