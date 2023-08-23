"""Solves the puzzle for Day 16 of Advent of Code 2019.

Flawed Frequency Transmission

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/16
"""
from itertools import accumulate, cycle, islice
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 16
    TITLE = "Flawed Frequency Transmission"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"\d", int_processor), delimiter=""
        )

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        data = list(self.input)

        patterns = [
            list(
                islice(
                    cycle(
                        ([0] * (i + 1))
                        + ([1] * (i + 1))
                        + ([0] * (i + 1))
                        + ([-1] * (i + 1))
                    ),
                    1,
                    len(data),
                )
            )
            for i in range(len(data))
        ]

        for _ in range(100):
            data = [
                abs(sum(x * p for x, p in zip(data, patterns[i]))) % 10
                for i in range(len(data))
            ]

        return "".join(map(str, data[:8]))

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        # solved with a little help from Advent of Coders on reddit
        offset = int("".join(map(str, self.input[:7])))
        data = (self.input * 10000)[-1 : offset - 1 : -1]

        for _ in range(100):
            data = [x % 10 for x in accumulate(data)]

        return "".join(map(str, data[-1:-9:-1]))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
