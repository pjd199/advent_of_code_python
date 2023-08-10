"""Solves the puzzle for Day 20 of Advent of Code 2017.

Particle Swarm

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/20
"""
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass(eq=True, order=True)
class _Point:
    """Represents a 3D point."""

    x: int
    y: int
    z: int

    def __init__(self, text: str):
        """Initialise the Point from a string.

        Args:
            text (str): the comma delimiter string
        """
        self.x, self.y, self.z = [int(a) for a in text.split(",")]

    def dist(self) -> int:
        """Calculates 3D Manhattan distance from (0,0,0).

        Returns:
            int: the distance
        """
        return abs(self.x) + abs(self.y) + abs(self.z)

    def add(self, other: "_Point") -> None:
        """Add a Point to this Point.

        Args:
            other ("_Point"): the other point
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z


@dataclass
class _Particle:
    """Represents a particle."""

    position: _Point
    velocity: _Point
    acceleration: _Point

    def tick(self) -> None:
        self.velocity.add(self.acceleration)
        self.position.add(self.velocity)


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 20
    TITLE = "Particle Swarm"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                r"p=<(?P<position>[0-9\-,]+)>, "
                r"v=<(?P<velocity>[0-9\-,]+)>, "
                r"a=<(?P<acceleration>[0-9\-,]+)>",
                dataclass_processor(_Particle),
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        particles = deepcopy(self.input)

        # run the simulation
        for _ in range(500):
            for p in particles:
                p.tick()

        # find the index of the nearest particle
        _, min_index = sorted(
            [(d, i) for i, d in enumerate([p.position.dist() for p in particles])]
        )[0]

        return min_index

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        particles = deepcopy(self.input)

        # run the simulation
        for _ in range(500):
            for p in particles:
                p.tick()

            # check for collisions
            particles.sort(key=lambda x: x.position)
            i = 0
            while i < len(particles) - 1:
                if particles[i].position == particles[i + 1].position:
                    end = i + 2
                    while (
                        end < len(particles)
                        and particles[i].position == particles[end].position
                    ):
                        end += 1
                    del particles[i:end]
                else:
                    i += 1

        return len(particles)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
