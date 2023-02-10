"""Simualte an IntCode Computer, as part of Advent of Code 2019."""
from collections import deque
from copy import deepcopy
from enum import Enum, unique
from typing import Callable, Deque, Dict, List, Tuple

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line


@unique
class Action(Enum):
    """Action for the operation result."""

    write = 0
    output = 1
    jump = 2
    terminate = 3


class IntcodeComputer:
    """Emulate the Intcode Computer."""

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initalise the computer witht he given puzzle_input.

        Args:
            puzzle_input (List[str]): the input data
        """
        self.program_source = parse_tokens_single_line(
            puzzle_input, (r"-?\d+", int_processor), delimiter=","
        )
        self.input_buffer: Deque[int] = deque()
        self.output_buffer: Deque[int] = deque()
        self.reset()

    def reset(self) -> None:
        """Reset the Intcode Computer for another run."""
        self.program = deepcopy(self.program_source)
        self.input_buffer.clear()
        self.output_buffer.clear()
        self.pointer = 0
        self.terminated = False

    def append_input(self, value: int) -> None:
        """Add a single input value to the input buffer.

        Args:
            value (int): the value to add
        """
        self.input_buffer.append(value)

    def read_output(self) -> int:
        """Read a single output value from the output buffer.

        Returns:
            int: _description_
        """
        return self.output_buffer.popleft()

    def direct_memory_access(self) -> List[int]:
        """Access the computer's memory.

        Returns:
            List[int]: the memory registers
        """
        return self.program

    def has_terminated(self) -> bool:
        """Termination flag.

        Returns:
            bool: returns True if the program has terminated, otherwise False
        """
        return self.terminated

    def execute(self, break_on_output: bool = False) -> None:
        """Execute the program.

        Args:
            break_on_output (bool): if True, returns when an output is generated.

        Raises:
            RuntimeError: if the program has already finished
        """
        if self.terminated:  # pragma: no cover
            raise RuntimeError("Program has terminated")

        # define the instructions
        instructions: Dict[int, Tuple[int, Callable[[List[int]], int], Action]] = {
            1: (3, lambda p: p[0] + p[1], Action.write),
            2: (3, lambda p: p[0] * p[1], Action.write),
            3: (1, lambda _: self.input_buffer.popleft(), Action.write),
            4: (1, lambda p: p[0], Action.output),
            5: (2, lambda p: p[1] if p[0] != 0 else self.pointer + 3, Action.jump),
            6: (2, lambda p: p[1] if p[0] == 0 else self.pointer + 3, Action.jump),
            7: (3, lambda p: 1 if p[0] < p[1] else 0, Action.write),
            8: (3, lambda p: 1 if p[0] == p[1] else 0, Action.write),
            99: (0, lambda _: 0, Action.terminate),
        }

        # execute the program
        while True:
            # decode the opcode and parameters
            opcode = self.program[self.pointer] % 100
            length, operator, action = instructions[opcode]
            modes = [
                ((self.program[self.pointer] // (10**x)) % 10) for x in range(2, 5)
            ]
            params = [
                self.program[self.pointer + j + 1]
                if modes[j]
                else self.program[self.program[self.pointer + j + 1]]
                for j in range(length)
            ]

            # execute the instruction
            value = operator(params)
            if action == Action.write:
                self.program[self.program[self.pointer + length]] = value
                self.pointer += length + 1
            elif action == Action.output:
                self.output_buffer.append(value)
                self.pointer += length + 1
                if break_on_output:
                    break
            elif action == Action.jump:
                self.pointer = value
            elif action == Action.terminate:
                self.terminated = True
                break
