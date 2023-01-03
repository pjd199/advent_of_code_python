"""Solves the puzzle for Day 19 of Advent of Code 2022.

Not Enough Minerals

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/19
"""
from dataclasses import dataclass
from math import ceil, prod
from pathlib import Path
from sys import maxsize, path
from typing import Dict, List, Tuple

from lambda_multiprocessing import Pool  # type: ignore

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


@dataclass
class _Blueprint:
    """A blueprint from the input."""

    identifier: int
    robots: Tuple[  # ore, clay, obsidian, geode
        Tuple[int, int, int, int],
        Tuple[int, int, int, int],
        Tuple[int, int, int, int],
        Tuple[int, int, int, int],
    ]
    max_materials: Tuple[int, int, int, int]


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 19
    TITLE = "Not Enough Minerals"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        parsed = parse_lines(
            puzzle_input,
            (
                r"Blueprint (\d+): "
                r"Each ore robot costs (\d+) ore. "
                r"Each clay robot costs (\d+) ore. "
                r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
                r"Each geode robot costs (\d+) ore and (\d+) obsidian.",
                int_tuple_processor,
            ),
        )
        self.input = [
            _Blueprint(
                x[0],
                (
                    (x[1], 0, 0, 0),
                    (x[2], 0, 0, 0),
                    (x[3], x[4], 0, 0),
                    (x[5], 0, x[6], 0),
                ),
                (max(x[1], x[2], x[3], x[5]), x[4], x[6], maxsize),
            )
            for x in parsed
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        with Pool() as pool:
            results = pool.starmap(
                self._solve,
                ((b, (0, 0, 0, 0), (1, 0, 0, 0), 24, {}) for b in self.input),
            )
        return sum(b.identifier * result for b, result in zip(self.input, results))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        with Pool() as pool:
            results = pool.starmap(
                self._solve,
                ((b, (0, 0, 0, 0), (1, 0, 0, 0), 32, {}) for b in self.input[:3]),
            )
        return int(prod(results))

    def _solve(
        self,
        blueprint: _Blueprint,
        materials: Tuple[int, ...],
        robots: Tuple[int, ...],
        time: int,
        best: Dict[int, int],
    ) -> int:
        """Recusively solve the puzzle, focusing on the next robot to build.

        Args:
            blueprint (_Blueprint): the blueprint to solve
            materials (Tuple[int, int, int, int]): the current materials
            robots (Tuple[int, int, int, int]): the current robots
            time (int): the remaining time
            best (Dict[int, int]): mapping of seconds remaining to best geode produced

        Returns:
            int: the best result (highest number of geodes)
        """
        # abandon path if behind best path
        if materials[GEODE] < best.get(time + 1, 0):
            return 0

        # record the best path results for far
        if materials[GEODE] > 0:
            best[time] = max(best.get(time, 0), materials[GEODE])

        # initialise results with the result of not building any more robots
        results = [materials[GEODE] + (robots[GEODE] * time)]

        # build robots, if possible
        for robot_to_build in [ORE, CLAY, OBSIDIAN, GEODE]:
            if robots[robot_to_build] < blueprint.max_materials[robot_to_build]:
                # calculate time to get mine enough material to build robot,
                # using maxsize as infinity
                delta = max(
                    max(0, ceil((b - m) / r)) if r > 0 else maxsize
                    for r, m, b in zip(
                        robots, materials, blueprint.robots[robot_to_build]
                    )
                    if b > 0
                )

                # if we have enough time to build and use the robot before time is up,
                # then build the robot
                if time - delta > 1:
                    results.append(
                        self._solve(
                            blueprint,
                            tuple(
                                m + (r * (delta + 1)) - b
                                for m, r, b in zip(
                                    materials,
                                    robots,
                                    blueprint.robots[robot_to_build],
                                )
                            ),
                            tuple(
                                r + (1 if i == robot_to_build else 0)
                                for i, r in enumerate(robots)
                            ),
                            time - delta - 1,
                            best,
                        )
                    )

        return max(results)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
