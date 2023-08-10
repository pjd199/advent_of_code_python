"""Solves the puzzle for Day 3 of Advent of Code 2016.

Squares With Three Sides

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from itertools import chain
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 3
    TITLE = "Squares With Three Sides"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input, (r"[0-9]+", int_processor), delimiter=r"\s+"
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._count_possbile_triangles(self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._count_possbile_triangles(
            list(
                chain.from_iterable(
                    [
                        [
                            [x[0][0], x[1][0], x[2][0]],
                            [x[0][1], x[1][1], x[2][1]],
                            [x[0][2], x[1][2], x[2][2]],
                        ]
                        for x in zip(
                            self.input[::3], self.input[1::3], self.input[2::3]
                        )
                    ]
                )
            )
        )

    def _count_possbile_triangles(self, itr: List[List[int]]) -> int:
        """Count the number of possible trianges.

            For possible triangles, the sum of two sides is greater than
            the length of the third side

        Args:
            itr (List[List[int]]): the input

        Returns:
            int: the count
        """
        return len(
            [
                x
                for x in itr
                if (x[0] + x[1] > x[2])
                and (x[1] + x[2] > x[0])
                and (x[2] + x[0] > x[1])
            ]
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
