"""Solves the puzzle for Day 13 of Advent of Code 2023.

Point of Incidence

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/13
"""
from pathlib import Path
from sys import path

import numpy as np
import numpy.typing as npt

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, split_sections, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 13
    TITLE = "Point of Incidence"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = [
            np.array(parse_tokens(section, (r"[.#]", str_processor)), dtype="str")
            for section in split_sections(puzzle_input)
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self.summarize(pattern) for pattern in self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self.summarize(pattern, 1) for pattern in self.input)

    def summarize(self, pattern: npt.NDArray[np.str_], smudge: int = 0) -> int:
        """Summarise the pattern.

        Args:
            pattern (npt.NDArray[np.str_]): the pattern
            smudge (int): the smudge required level

        Returns:
            int: the result
        """
        result = 0
        # check for reflections on rows
        for i in range(len(pattern) - 1):
            if np.count_nonzero(pattern[i : i + 1] != pattern[i + 1 : i + 2]) <= smudge:
                size = min(i + 1, len(pattern) - i - 1)
                if (
                    np.count_nonzero(
                        pattern[i - size + 1 : i + 1] != pattern[i + size : i : -1]
                    )
                    == smudge
                ):
                    result += (i + 1) * 100

        # check for reflections on columns
        for i in range(len(pattern[0]) - 1):
            if (
                np.count_nonzero(pattern[:, i : i + 1] != pattern[:, i + 1 : i + 2])
                <= smudge
            ):
                size = min(i + 1, len(pattern[0]) - i - 1)
                if (
                    np.count_nonzero(
                        pattern[:, i - size + 1 : i + 1]
                        != pattern[:, i + size : i : -1]
                    )
                    == smudge
                ):
                    result += i + 1

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
