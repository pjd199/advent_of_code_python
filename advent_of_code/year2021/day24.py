"""Solves the puzzle for Day 24 of Advent of Code 2021.

Arithmetic Logic Unit

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/24
"""
from itertools import chain
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 24
    TITLE = "Arithmetic Logic Unit"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input,
            (r"(inp|add|mul|div|mod|eql|w|x|y|z|-?\d+)", str_processor),
            delimiter=" ",
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve()[1]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve()[0]

    def _solve(self) -> tuple[int, int]:
        """Solve the puzzle.

        Returns:
            tuple[int, int]: the answers - (smallest, largest)
        """
        # extract the rules from the input
        data = [
            (int(self.input[i + 5][-1]), int(self.input[i + 15][-1]))
            for i in range(0, len(self.input), 18)
        ]

        # use the input data to create the rules list
        rules = []
        stack = []
        for i, (check, offset) in enumerate(data):
            if check > 0:
                stack.append((i, offset))
            else:
                j, prev_offset = stack.pop()
                diff = prev_offset + check
                rules.append((j, i, -diff) if diff < 0 else (i, j, diff))

        # work out the digits of the smallest and largest valid number
        smallest_list = [((i, 1 + diff), (j, 1)) for i, j, diff in rules]
        largest_list = [((i, 9), (j, 9 - diff)) for i, j, diff in rules]

        smallest, largest = tuple(
            int("".join([str(x[1]) for x in sorted(chain.from_iterable(x))]))
            for x in [smallest_list, largest_list]
        )

        # flatten each list of digits into the digits of a int, and return them
        return smallest, largest


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
