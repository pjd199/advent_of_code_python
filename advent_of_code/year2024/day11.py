"""Solves the puzzle for Day 11 of Advent of Code 2024.

Plutonian Pebbles

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/11
"""

from functools import cache

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 11
    TITLE = "Plutonian Pebbles"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"\d+", int_processor), delimiter=" "
        )

    def _solve(self, repeat: int) -> int:
        """Solve the puzzle.

        Args:
            repeat (int): number of repeats

        Returns:
            int: the result
        """

        @cache
        def split(n: int) -> tuple[int, int]:
            s = str(n)
            return int(s[: len(s) // 2]), int(s[len(s) // 2 :])

        @cache
        def simulate(stone: int, repeat: int) -> int:
            if repeat == 0:
                return 1
            if stone == 0:
                return simulate(1, repeat - 1)
            if stone == 1:
                return simulate(2024, repeat - 1)
            if len(str(stone)) % 2 == 0:
                left, right = split(stone)
                return simulate(left, repeat - 1) + simulate(right, repeat - 1)
            return simulate(stone * 2024, repeat - 1)

        return sum(simulate(stone, repeat) for stone in self.input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(repeat=25)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(repeat=75)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
