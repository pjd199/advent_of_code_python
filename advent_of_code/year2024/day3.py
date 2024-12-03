"""Solves the puzzle for Day 3 of Advent of Code 2024.

Mull It Over

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/3
"""

from pathlib import Path
from re import findall
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 3
    TITLE = "Mull It Over"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"(.*mul\(\d+,\d+\).*)+", str_processor)
        )

    def solve(self, check_enabled: bool) -> int:
        """Solve the puzzle.

        Args:
            check_enabled (bool): if true, check for enable/disable

        Returns:
            int: the result
        """
        result = 0
        enabled = True
        for line in self.input:
            for a, b, enable, disable in findall(
                r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))",
                line,
            ):
                if enable:
                    enabled = True
                elif disable:
                    enabled = False
                elif enabled or not check_enabled:
                    result += int(a) * int(b)
        return result

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self.solve(check_enabled=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self.solve(check_enabled=True)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
