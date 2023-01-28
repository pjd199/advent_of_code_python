"""Solves the puzzle for Day 2 of Advent of Code 2019.

1202 Program Alarm

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/2
"""
from itertools import product
from operator import add, mul
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 2
    TITLE = "1202 Program Alarm"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"\d+", int_processor), delimiter=","
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._execute(12, 2)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return next(
            (100 * noun) + verb
            for noun, verb in product(range(100), range(100))
            if self._execute(noun, verb) == 19690720
        )

    def _execute(self, noun: int, verb: int) -> int:
        """Execute the program.

        Args:
            noun (int): the first input
            verb (int): the second input

        Returns:
            int: the output
        """
        # duplicate the program and set the inputs
        program = list(self.input)
        program[1] = noun
        program[2] = verb

        # load the operators
        operators = {1: add, 2: mul}

        # run the program
        i = 0
        while program[i] != 99:
            opcode, a, b, c = program[i : i + 4]
            program[c] = operators[opcode](program[a], program[b])
            i += 4

        # return the result
        return program[0]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
