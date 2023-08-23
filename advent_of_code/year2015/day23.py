"""Solves the puzzle for Day 23 of Advent of Code 2015.

Opening the Turing Lock

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/23
"""
from dataclasses import dataclass
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 23
    TITLE = "Opening the Turing Lock"

    @dataclass
    class Line:
        """A Line of he program."""

        instruction: str
        register: str = ""
        offset: int = 0

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the solver.

        Args:
            puzzle_input (list[str]): the puzzle input
        """
        self.program = parse_lines(
            puzzle_input,
            (
                r"(?P<instruction>[a-z]+) "
                r"(?P<register>[ab])?([, ]*)?"
                r"(?P<offset>[\+\-0-9]+)?",
                dataclass_processor(Solver.Line),
            ),
        )

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one.

        Returns:
            int: the answer
        """
        return self._run(a=0, b=0)

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part one.

        Returns:
            int: the results
        """
        return self._run(a=1, b=0)

    def _run(self, a: int = 0, b: int = 0) -> int:
        """Execute the input program.

        Args:
            a (int): The initial value of register "a". Default is 0
            b (int): The initial value of register "b". Default is 0

        Returns:
            int: The value of register "b" at the end of the program
        """
        memory = {"a": a, "b": b}
        i = 0
        while i >= 0 and i < len(self.program):
            if self.program[i].instruction == "hlf":  # half
                memory[self.program[i].register] //= 2
                i += 1
            elif self.program[i].instruction == "tpl":  # triple
                memory[self.program[i].register] *= 3
                i += 1
            elif self.program[i].instruction == "inc":  # increament
                memory[self.program[i].register] += 1
                i += 1
            elif self.program[i].instruction == "jmp":  # jump
                i += int(self.program[i].offset)
            elif self.program[i].instruction == "jie":  # jump if even
                i += (
                    int(self.program[i].offset)
                    if (memory[self.program[i].register] % 2 == 0)
                    else 1
                )
            elif self.program[i].instruction == "jio":  # jump if one
                i += (
                    int(self.program[i].offset)
                    if (memory[self.program[i].register] == 1)
                    else 1
                )
        return memory["b"]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
