"""Solves the puzzle for Day 12 of Advent of Code 2019.

The N-Body Problem

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/12
"""
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import permutations
from math import lcm
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 12
    TITLE = "The N-Body Problem"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = [
            Moon(list(m))
            for m in parse_lines(
                puzzle_input,
                (
                    r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>",
                    int_tuple_processor,
                ),
            )
        ]
        self.input_tuples = parse_lines(
            puzzle_input,
            (
                r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>",
                int_tuple_processor,
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        jupiter = Planet(deepcopy(self.input))
        for _ in range(1000):
            jupiter.tick()

        return sum(
            sum(abs(a) for a in m.position) * sum(abs(a) for a in m.velocity)
            for m in jupiter.moons
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        jupiter = Planet(deepcopy(self.input))
        cycles = [0, 0, 0]  # [x, y, z]
        tick = 0

        while not all(i for i in cycles):
            jupiter.tick()
            tick += 1

            # look for the cycle half way point, when all velocities on the axis are 0
            for a in range(3):
                if not cycles[a] and all(not m.velocity[a] for m in jupiter.moons):
                    cycles[a] = tick * 2

        # return the lowest common multiple of the cycle lengths, ie the first time
        # all three axis are back to their starting positions
        return lcm(*cycles)


@dataclass
class Moon:
    """A Moon."""

    position: List[int]
    velocity: List[int] = field(default_factory=lambda: [0, 0, 0])

    def apply_gravity(self, other: "Moon") -> None:
        """Apply gravity to this moon based on position of other.

        Args:
            other (Moon): the other moon
        """
        self.velocity = [
            v if s == o else v + (1 if s < o else -1)
            for (s, o, v) in zip(self.position, other.position, self.velocity)
        ]

    def tick(self) -> None:
        """Move one tick in time."""
        self.position = [p + v for p, v in zip(self.position, self.velocity)]


@dataclass
class Planet:
    """A planet."""

    moons: List[Moon]

    def tick(self) -> None:
        """Tick the time forward."""
        for a, b in permutations(self.moons, 2):
            a.apply_gravity(b)
        for m in self.moons:
            m.tick()


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
