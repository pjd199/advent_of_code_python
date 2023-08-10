"""Solves the puzzle for Day 19 of Advent of Code 2021.

Beacon Scanner

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/19
"""
from itertools import permutations, product
from pathlib import Path
from sys import path
from typing import Generator

import numpy as np
from numpy.typing import NDArray

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines, split_sections
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 19
    TITLE = "Beacon Scanner"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = [
            parse_lines(
                section,
                (r"(-?\d+),(-?\d+),(-?\d+)", int_tuple_processor),
                header=(r"--- scanner \d+ ---",),
            )
            for section in split_sections(puzzle_input)
        ]
        self.beacons: set[tuple[int, int, int]] = set()
        self.locations: dict[int, NDArray[np.int_]] = {}

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._solve()
        return len(self.beacons)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._solve()
        locations = list(self.locations.values())
        return max(
            int(np.max(np.sum(np.abs(locations - x), axis=1))) for x in locations
        )

    def _solve(self) -> None:
        """Solve the puzzle by locating the beacons."""
        if self.beacons:
            return

        # create a rotation independant fingerprint for each scanner, which
        # is formed by the manhattan distance between each element in the array
        scanners = [np.array(x) for x in self.input]
        fingerprints = [
            set(np.sum(np.abs(scanner[:, np.newaxis] - scanner), axis=2).reshape(-1))
            for scanner in scanners
        ]

        # create pairs of neighbours, sorted by the likelyhood of a
        # fingerprint match
        neighbours = [
            x
            for _, x in sorted(
                {
                    (len(fingerprints[a] & fingerprints[b]), frozenset({a, b}))
                    for a, b in permutations(range(len(fingerprints)), 2)
                },
                reverse=True,
            )
        ]

        # prepare to align each of the scanners
        aligned = [np.array([]) for _ in range(len(scanners))]
        aligned[0] = scanners[0]
        self.locations = {0: np.array([0, 0, 0])}
        visited = {0}

        while len(self.locations) < len(scanners):
            # search through the ordered list of neighbours, choosing
            # the best match for a scanner not yet located
            for pair in (p for p in neighbours if len(p & visited) == 1):
                a = set(pair & visited).pop()
                b = set(pair - {a}).pop()

                # rotate until we find a common offset between 12 beacons.
                # A match is found when 12 vectors offsets match
                for rotation in self._rotations(scanners[b]):
                    # calculate all the offset vectors
                    vectors = aligned[a] - rotation[:, np.newaxis]
                    # find any multiple locations
                    pairs, counts = np.unique(
                        vectors.reshape(-1, 3), axis=0, return_counts=True
                    )
                    max_index = counts.argmax()
                    if counts[max_index] >= 12:
                        # store the aligned locations
                        offset = pairs[max_index]
                        aligned[b] = rotation + np.array(offset)
                        self.locations[b] = np.array(offset)
                        visited.add(b)
                        break
                break

        # find all the unique beacons
        self.beacons = {
            (x, y, z)
            for i, aligned_scanner in enumerate(aligned)
            for x, y, z in aligned_scanner
        }

    def _rotations(
        self, array: NDArray[np.int_]
    ) -> Generator[NDArray[np.int_], None, None]:
        for x, y, z in permutations([0, 1, 2]):
            for sx, sy, sz in product([-1, 1], repeat=3):
                rotation_matrix = np.zeros((3, 3), dtype=np.int_)
                rotation_matrix[0, x] = sx
                rotation_matrix[1, y] = sy
                rotation_matrix[2, z] = sz
                if np.linalg.det(rotation_matrix) == 1:
                    yield array @ rotation_matrix.T


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
