"""Solution for day 14 of Advent of Code 2015."""
from collections import namedtuple
from itertools import cycle
from re import compile
from typing import List, Tuple

from advent_of_code.utils.solver_interface import SolverInterface

Reindeer = namedtuple("Reindeer", "name speed flying resting")


class Solver(SolverInterface):
    """Solver for the puzzle."""

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if puzzle_input is None or len(puzzle_input) == 0:
            raise RuntimeError("Puzzle input is empty")

        pattern = compile(
            r"(?P<name>[A-Za-z]+) can fly "
            r"(?P<speed>[0-9]+) km/s for "
            r"(?P<flying>[0-9]+) seconds, "
            r"but then must rest for "
            r"(?P<resting>[0-9]+) seconds."
        )
        self.herd = []
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                self.herd.append(
                    Reindeer(
                        name=match["name"],
                        speed=int(match["speed"]),
                        flying=int(match["flying"]),
                        resting=int(match["resting"]),
                    )
                )
            else:
                raise RuntimeError(f"Parse error on line {i + 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        positions, _ = self._race()
        return max(positions)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        _, points = self._race()
        return max(points)

    def solve_all(self) -> List[int]:
        """Solve both parts of the puzzle.

        Returns:
            List[int]: the answer
        """
        positions, points = self._race()
        return [max(positions), max(points)]

    def _race(self) -> Tuple[List[int], List[int]]:
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
