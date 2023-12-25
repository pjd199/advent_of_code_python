"""Solves the puzzle for Day 14 of Advent of Code 2023.

Parabolic Reflector Dish

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/14
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

import numpy as np
import numpy.typing as npt

from advent_of_code.utils.parser import parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 14
    TITLE = "Parabolic Reflector Dish"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.lookup = {"O": 0, ".": 1, "#": 2}
        self.input = np.array(
            parse_tokens(
                puzzle_input, (r"[O#.]", lambda m: self.lookup[m[0]]), delimiter=""
            ),
            dtype="int",
        )

    def tilt(
        self, platform: npt.NDArray[np.int_], direction: int = 0
    ) -> npt.NDArray[np.int_]:
        """Tilt the platform.

        Args:
            platform (npt.NDArray[np.int_]): the input platform
            direction (int): the tilk 0=N, 1=W, 2=S, 3=E

        Returns:
            npt.NDArray[np.int_]: the result
        """
        rotation = [1, 0, -1, -2][direction]
        return np.rot90(
            np.row_stack(
                [
                    np.concatenate(
                        [
                            np.sort(x)
                            for x in np.hsplit(
                                row, np.nonzero(row == self.lookup["#"])[0] + 1
                            )
                        ]
                    )
                    for row in np.rot90(platform, rotation)
                ]
            ),
            -rotation,
        )

    def calculate_load(self, platform: npt.NDArray[np.int_]) -> int:
        """Calculate the load on the north wall.

        Args:
            platform (npt.NDArray[np.int_]): the platform

        Returns:
            int: the loading
        """
        return int(
            np.sum(
                np.count_nonzero(platform == self.lookup["O"], axis=1)
                * np.arange(len(platform), 0, -1)
            )
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self.calculate_load(self.tilt(self.input))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        target = 1000000000
        platform = self.input
        states = {platform.tobytes(): 0}
        results = [platform]
        cycle = 1
        while cycle < target:
            for direction in range(4):
                platform = self.tilt(platform, direction)
            key = platform.tobytes()
            if key in states:
                break
            states[key] = cycle
            results.append(platform)
            cycle += 1

        platform = results[states[key] + (target - states[key]) % (cycle - states[key])]

        return self.calculate_load(platform)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
