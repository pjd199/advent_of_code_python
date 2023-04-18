"""Solves the puzzle for Day 8 of Advent of Code 2021.

Seven Segment Search

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/8
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 8
    TITLE = "Seven Segment Search"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = [
            ([frozenset(x) for x in a.split()], [frozenset(x) for x in b.split()])
            for a, b in parse_lines(
                puzzle_input, (r"([a-z ]+) \| ([a-z ]+)", str_tuple_processor)
            )
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1
            for _, digits in self.input
            for digit in digits
            if len(digit) in [2, 4, 3, 7]
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        total = 0
        for patterns, digits in self.input:
            # easy mapping based on length
            mapping = {
                1: next(x for x in patterns if len(x) == 2),
                4: next(x for x in patterns if len(x) == 4),
                7: next(x for x in patterns if len(x) == 3),
                8: next(x for x in patterns if len(x) == 7),
            }

            # work out the horizontal segments in the display
            cross_bars = frozenset.intersection(*[x for x in patterns if len(x) == 5])
            top = cross_bars & mapping[7]
            middle = cross_bars & mapping[4]
            bottom = cross_bars - top - middle

            # work out more mapping using the crossbars
            mapping[0] = mapping[8] - middle
            mapping[3] = cross_bars | mapping[1]
            mapping[9] = mapping[4] | top | bottom
            mapping[6] = frozenset(
                next(
                    x
                    for x in patterns
                    if len(x) == 6 and set(x) != mapping[9] and set(x) != mapping[0]
                )
            )

            # find lower left and upper right to finish the mapping
            lower_left = mapping[8] - mapping[9]
            mapping[5] = mapping[6] - lower_left
            upper_right = mapping[1] - mapping[6]
            mapping[2] = cross_bars | upper_right | lower_left

            # invert the mapping, decode each digit,
            # then add that number to the running total
            decoder = {v: str(k) for k, v in mapping.items()}
            total += int("".join([decoder[digit] for digit in digits]))

        return total


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
