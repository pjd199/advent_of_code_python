"""Solves the puzzle for Day 8 of Advent of Code 2020.

Handheld Halting

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/8
"""
from copy import deepcopy
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 8
    TITLE = "Handheld Halting"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = [
            (word, int(num))
            for word, num in parse_lines(
                puzzle_input, (r"(nop|acc|jmp) ([+-]\d+)", str_tuple_processor)
            )
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        _, accumulator = self._loop_detector(self.input)
        return accumulator

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        program = deepcopy(self.input)
        result = -1
        for i, (instruction, value) in enumerate(self.input):
            if instruction == "acc":
                continue

            program[i] = ("jmp" if instruction == "nop" else "nop", value)
            loop, accumulator = self._loop_detector(program)
            program[i] = (instruction, value)
            if not loop:
                result = accumulator
                break

        return result

    def _loop_detector(self, program: list[tuple[str, int]]) -> tuple[bool, int]:
        """Detect a loop in the given program.

        Args:
            program (list[tuple[str, int]]): the input program

        Returns:
            tuple[bool, int]: the results (loop detected, accumulator value)
        """
        pointer = 0
        accumulator = 0
        visited: set[int] = set()
        loop_detected = False

        while 0 <= pointer < len(program):
            instruction, value = program[pointer]
            if instruction == "acc":
                accumulator += value
                pointer += 1
            elif instruction == "jmp":
                pointer += value
            else:
                pointer += 1

            if pointer in visited:
                loop_detected = True
                break
            visited.add(pointer)

        return loop_detected, accumulator


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
