"""Solves the puzzle for Day 23 of Advent of Code 2016.

Safe Cracking

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/23
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2016.assembunny import Action, Instruction, load, run


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 23
    TITLE = "Safe Cracking"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.program = load(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return run(self.program, a=7)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # run with loop optimisation
        return run(
            self.program[:4]
            + [
                Instruction(Action.COPY, "1", "a"),
                Instruction(Action.MULTIPLY, "a", "b"),
                Instruction(Action.MULTIPLY, "a", "d"),
                Instruction(Action.COPY, "0", "c"),
                Instruction(Action.COPY, "0", "d"),
                Instruction(Action.NOP, "0", "0"),
            ]
            + self.program[10:],
            a=12,
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
