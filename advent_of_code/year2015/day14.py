"""Solves the puzzle for Day 14 of Advent of Code 2015.

Reindeer Olympics

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/14
"""
from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Reindeer:
    """A reindeer."""

    name: str
    speed: int
    flying: int
    resting: int


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 14
    TITLE = "Reindeer Olympics"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file

        """
        self.herd = parse_lines(
            puzzle_input,
            (
                r"(?P<name>[A-Za-z]+) can fly "
                r"(?P<speed>[0-9]+) km/s for "
                r"(?P<flying>[0-9]+) seconds, but then must rest for "
                r"(?P<resting>[0-9]+) seconds.",
                dataclass_processor(Reindeer),
            ),
        )

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        positions, _ = self._race()
        return max(positions)

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        _, points = self._race()
        return max(points)

    @cache_result
    def _race(self) -> tuple[list[int], list[int]]:
        # positions will hold the current position of each reindeer
        # points will hold the current points of each reindeer
        # iterators will hold a iterator, which returns the current speed
        # in the flying / resting cycle
        positions = [0] * len(self.herd)
        points = [0] * len(self.herd)
        iterators = [
            cycle(([reindeer.speed] * reindeer.flying) + ([0] * reindeer.resting))
            for reindeer in self.herd
        ]

        # run the simulation, second by second, til the end of the race
        for _ in range(2503):
            positions = [positions[x] + next(i) for x, i in enumerate(iterators)]
            leader = max(positions)
            points = [
                points[i] + 1 if position == leader else points[i]
                for i, position in enumerate(positions)
            ]

        return positions, points


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
