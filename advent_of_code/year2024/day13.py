"""Solves the puzzle for Day 13 of Advent of Code 2024.

Claw Contraption

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/13
"""

from advent_of_code.utils.parser import (
    int_sequence_processor,
    parse_lines,
    split_sections,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 13
    TITLE = "Claw Contraption"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input)
        self.input = [
            parse_lines(
                section,
                (r"Button [AB]: X\+(\d+), Y\+(\d+)", int_sequence_processor),
                (r"Prize: X=(\d+), Y=(\d+)", int_sequence_processor),
            )
            for section in sections
        ]

    def _solve(self, offset: int) -> int:
        """Solve the puzzle using linear equations.

        Args:
            offset (int): target x,y offset

        Returns:
            int: the total cost
        """
        result = 0
        for (xa, ya), (xb, yb), (xt, yt) in self.input:
            xt += offset
            yt += offset
            a, arem = divmod((xb * yt - yb * xt), (xb * ya - yb * xa))
            b, brem = divmod((xt - xa * a), xb)
            if arem == 0 and brem == 0:
                result += 3 * a + b
        return result

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(0)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(10000000000000)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
