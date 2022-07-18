"""Solves the puzzle for Day 3 of Advent of Code 2016."""
from itertools import chain
from re import compile
from typing import Iterable, List

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        self.input = []
        pattern = compile(r"(?P<a>[0-9]+)\s+(?P<b>[0-9]+)\s+(?P<c>[0-9]+)")
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.input.append([int(m["a"]), int(m["b"]), int(m["c"])])
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i}")

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
            chain.from_iterable(
                [
                    [
                        [x[0][0], x[1][0], x[2][0]],
                        [x[0][1], x[1][1], x[2][1]],
                        [x[0][2], x[1][2], x[2][2]],
                    ]
                    for x in zip(self.input[::3], self.input[1::3], self.input[2::3])
                ]
            )
        )

    def _count_possbile_triangles(self, itr: Iterable[List[List[int]]]) -> int:
        """Count the number of possible trianges.

            For possible triangles, the sum of two sides is greater than
            the length of the third side

        Args:
            itr (Iterable[List[List[int]]]): the input

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
