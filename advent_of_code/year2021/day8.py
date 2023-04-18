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
            # easy mappings based on length
            mappings = {
                1: next(x for x in patterns if len(x) == 2),
                4: next(x for x in patterns if len(x) == 4),
                7: next(x for x in patterns if len(x) == 3),
                8: next(x for x in patterns if len(x) == 7),
            }

            # work out the horizontal segments in the display
            cross_bars = frozenset.intersection(*[x for x in patterns if len(x) == 5])
            top = cross_bars & mappings[7]
            middle = cross_bars & mappings[4]
            bottom = cross_bars - top - middle

            # work out more mappings using the crossbars
            mappings[0] = mappings[8] - middle
            mappings[3] = cross_bars | mappings[1]
            mappings[9] = mappings[4] | top | bottom
            mappings[6] = frozenset(
                next(
                    x
                    for x in patterns
                    if len(x) == 6 and set(x) != mappings[9] and set(x) != mappings[0]
                )
            )

            # find lower left and upper right to finish the mappings
            lower_left = mappings[8] - mappings[9]
            mappings[5] = mappings[6] - lower_left
            upper_right = mappings[1] - mappings[6]
            mappings[2] = cross_bars | upper_right | lower_left

            # map the digits to a string, then add that number to the running total
            total += int(
                "".join(
                    [
                        str(next(k for k, v in mappings.items() if set(digit) == v))
                        for digit in digits
                    ]
                )
            )

        return total


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
