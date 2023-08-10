"""Solves the puzzle for Day 5 of Advent of Code 2017.

A Maze of Twisty Trampolines, All Alike

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/5
"""
from copy import deepcopy
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 5
    TITLE = "A Maze of Twisty Trampolines, All Alike"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"-?\d+", int_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        instructions = deepcopy(self.input)
        steps = 0

        i = 0
        while 0 <= i < len(instructions):
            offset = instructions[i]
            instructions[i] += 1
            i += offset
            steps += 1

        return steps

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        instructions = deepcopy(self.input)
        steps = 0

        i = 0
        while 0 <= i < len(instructions):
            offset = instructions[i]
            if offset < 3:
                instructions[i] += 1
            else:
                instructions[i] -= 1
            i += offset
            steps += 1

        return steps


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
