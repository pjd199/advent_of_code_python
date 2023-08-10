"""Solves the puzzle for Day 20 of Advent of Code 2022.

Grove Positioning System

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/20
"""
from collections import deque
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 20
    TITLE = "Grove Positioning System"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"-?[0-9]+", int_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve()

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(811589153, 10)

    def _solve(self, multiplier: int = 1, cycles: int = 1) -> int:
        """Solve the puzzle.

        Args:
            multiplier (int): mulitplier for the input
            cycles (int): number of mix cycles to perform

        Returns:
            int: the result
        """
        values = [x * multiplier for x in self.input]

        # seq in the index number of the values in the input
        seq = deque(range(len(self.input)))
        for _ in range(cycles):
            for i, x in enumerate(values):
                seq.rotate(-seq.index(i))
                seq.popleft()
                seq.rotate(-x)
                seq.appendleft(i)

        mixed = [values[i] for i in seq]
        index = mixed.index(0)
        return sum(mixed[(index + offset) % len(seq)] for offset in [1000, 2000, 3000])


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
