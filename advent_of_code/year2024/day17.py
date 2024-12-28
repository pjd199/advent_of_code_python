"""Solves the puzzle for Day 17 of Advent of Code 2024.

Chronospatial Computer

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/17
"""

from collections.abc import Sequence

from advent_of_code.utils.parser import (
    int_processor,
    parse_lines,
    parse_tokens_single_line,
    split_sections,
    str_sequence_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 17
    TITLE = "Chronospatial Computer"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        register, program = split_sections(puzzle_input, expected_sections=2)
        self.register = {
            name: int(value)
            for name, value in parse_lines(
                register, (r"Register ([ABC]): (\d+)", str_sequence_processor)
            )
        }
        self.program = parse_tokens_single_line(
            program,
            (r"\d+", int_processor),
            delimiter=r"Program: |,",
        )

    def _run(self, a: int, b: int, c: int) -> Sequence[int]:
        pointer = 0
        output = []

        while 0 <= pointer < len(self.program) - 1:
            opcode, operand = self.program[pointer : pointer + 2]
            combo = [0, 1, 2, 3, a, b, c]
            match opcode:
                case 0:  # adv
                    a = a // 2 ** combo[operand]
                    pointer += 2
                case 1:  # bxl
                    b = b ^ operand
                    pointer += 2
                case 2:  # bst
                    b = combo[operand] % 8
                    pointer += 2
                case 3:  # jnz
                    pointer = operand if a != 0 else pointer + 2
                case 4:  # bxc
                    b = b ^ c
                    pointer += 2
                case 5:  # out
                    output.append(combo[operand] % 8)
                    pointer += 2
                case 6:  # bdv
                    b = a // 2 ** combo[operand]
                    pointer += 2
                case 7:  # cdv
                    c = a // 2 ** combo[operand]
                    pointer += 2

        return output

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        return ",".join(str(x) for x in self._run(*self.register.values()))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        def search(target: list[int], prev_a: int) -> int:
            if len(target) == 0:
                return prev_a
            for a in range(1 << 10):
                if (a >> 3 == prev_a & 127) and self._run(a, 0, 0)[0] == target[-1]:
                    possible = search(target[:-1], prev_a << 3 | (a % 8))
                    if possible >= 0:
                        return possible
            return -1

        return search(self.program, 0)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
