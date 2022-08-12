"""Solution for day 23 of Advent of Code 2015."""
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 23
    TITLE = "Opening the Turing Lock"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the solver.

        Args:
            puzzle_input (List[str]): the puzzle input

        Raises:
            RuntimeError: raised for a parse error
        """
        self.program = []

        # validate input
        if puzzle_input is None or len(puzzle_input) == 0:
            raise RuntimeError("Puzzle input is empty")

        pattern = compile(
            r"^(?P<ins>[a-z]+) " r"(?P<reg>[ab])?([, ]*)?" r"(?P<off>[\+\-0-9]+)?$"
        )
        for line in puzzle_input:
            m = pattern.match(line)
            if m:
                self.program.append(m.groupdict())
            else:
                raise RuntimeError(f"Error on line: {line}")

    def solve_part_one(self) -> int:
        """Solve part one.

        Returns:
            int: the answer
        """
        return self._run(a=0, b=0)

    def solve_part_two(self) -> int:
        """Solve part one.

        Returns:
            int: the results
        """
        return self._run(a=1, b=0)

    def _run(self, a: int = 0, b: int = 0) -> int:
        # """Execute the input program.

        # Args:
        #     self: the object
        #     program (List[str]): The list of instructions
        #     a (int): The initial value of register "a". Default is 0
        #     b (int): The initial value of register "b". Default is 0

        # Raises:
        #     RuntimeError: If the input is invalid

        # Returns:
        #     int: The value of register "b" at the end of the program
        # """
        memory = {"a": a, "b": b}
        i = 0
        while i >= 0 and i < len(self.program):
            instruction = self.program[i]["ins"]
            register = self.program[i]["reg"]
            offset = self.program[i]["off"]
            if instruction == "hlf":  # half
                memory[register] //= 2
                i += 1
            elif instruction == "tpl":  # triple
                memory[register] *= 3
                i += 1
            elif instruction == "inc":  # increament
                memory[register] += 1
                i += 1
            elif instruction == "jmp":  # jump
                i += int(offset)
            elif instruction == "jie":  # jump if even
                i += int(offset) if (memory[register] % 2 == 0) else 1
            elif instruction == "jio":  # jump if one
                i += int(offset) if (memory[register] == 1) else 1
        return memory["b"]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
