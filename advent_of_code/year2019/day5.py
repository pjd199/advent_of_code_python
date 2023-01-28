"""Solves the puzzle for Day 5 of Advent of Code 2019.

Sunny with a Chance of Asteroids

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/5
"""
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Callable, Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Action(Enum):
    """Action for the operation result."""

    write = 0
    output = 1
    jump = 2
    terminate = 3


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 5
    TITLE = "Sunny with a Chance of Asteroids"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"-?\d+", int_processor), delimiter=","
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._execute(1)[-1]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._execute(5)[-1]

    def _execute(self, input_value: int) -> List[int]:
        """Execute the program.

        Args:
            input_value (int): the input value

        Returns:
            List[int]: the output
        """
        # ready the program and the output list
        program = list(self.input)
        outputs: List[int] = []

        # define the instructions
        instructions: Dict[int, Tuple[int, Callable[[List[int]], int], Action]] = {
            1: (3, lambda p: p[0] + p[1], Action.write),
            2: (3, lambda p: p[0] * p[1], Action.write),
            3: (1, lambda _: input_value, Action.write),
            4: (1, lambda p: p[0], Action.output),
            5: (2, lambda p: p[1] if p[0] != 0 else i + 3, Action.jump),
            6: (2, lambda p: p[1] if p[0] == 0 else i + 3, Action.jump),
            7: (3, lambda p: 1 if p[0] < p[1] else 0, Action.write),
            8: (3, lambda p: 1 if p[0] == p[1] else 0, Action.write),
            99: (0, lambda _: 0, Action.terminate),
        }

        # execute the program
        i = 0
        while True:
            # decode the opcode and parameters
            opcode = program[i] % 100
            length, operator, action = instructions[opcode]
            modes = [((program[i] // (10**x)) % 10) for x in range(2, 5)]
            params = [
                program[i + j + 1] if modes[j] else program[program[i + j + 1]]
                for j in range(length)
            ]

            # execute the instruction
            value = operator(params)
            if action == Action.write:
                program[program[i + length]] = value
                i += length + 1
            elif action == Action.output:
                outputs.append(value)
                i += length + 1
            elif action == Action.jump:
                i = value
            elif action == Action.terminate:
                break

        # return the results
        return outputs


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
