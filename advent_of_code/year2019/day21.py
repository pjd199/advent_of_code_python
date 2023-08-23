"""Solves the puzzle for Day 21 of Advent of Code 2019.

Springdroid Adventure

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/21
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 21
    TITLE = "Springdroid Adventure"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.computer = IntcodeComputer(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(
            "NOT A T",
            "NOT B J",
            "OR T J",
            "NOT C T",
            "OR T J",
            "AND D J",
            "WALK",
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(
            "NOT B J",
            "NOT C T",
            "OR T J",
            "AND D J",
            "AND H J",
            "NOT A T",
            "OR T J",
            "RUN",
        )

    def _solve(self, *script: str) -> int:
        """Solve the puzzle.

        Args:
            *script (str): the script to run

        Returns:
            int: the result
        """
        self.computer.reset()
        self.computer.input_data(*[ord(x) for x in "\n".join(script) + "\n"])
        self.computer.execute()
        return list(self.computer.iterate_output())[-1]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
