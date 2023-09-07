"""Simualte an IntCode Computer, as part of Advent of Code 2019."""
from collections import defaultdict, deque
from collections.abc import Callable, Iterator
from enum import Enum, unique

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line


@unique
class Action(Enum):
    """Action for the operation result."""

    write = 0
    output = 1
    jump = 2
    adjust_relative_base = 3
    terminate = 4


class IntcodeComputer:
    """Emulate the Intcode Computer."""

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initalise the computer witht he given puzzle_input.

        Args:
            puzzle_input (list[str]): the input data
        """
        self.program_source = parse_tokens_single_line(
            puzzle_input, (r"-?\d+", int_processor), delimiter=","
        )
        self._memory: defaultdict[int, int] = defaultdict(int)
        self._input_buffer: deque[int] = deque()
        self._output_buffer: deque[int] = deque()
        self.reset()

    def reset(self) -> None:
        """Reset the Intcode Computer for another run."""
        self._memory.clear()
        self._input_buffer.clear()
        self._output_buffer.clear()
        self._memory.update(enumerate(self.program_source))
        self._pointer = 0
        self._relative_base = 0
        self._terminated = False

    def input_data(self, *args: int) -> None:
        """Add values to the input buffer.

        Args:
            *args (int): the input values
        """
        self._input_buffer.extend(args)

    def read_output(self) -> int:
        """Read a single value from the output buffer.

        Returns:
            int: the next value from the output buffer
        """
        return self._output_buffer.popleft()

    def iterate_output(self) -> Iterator[int]:
        """Iterate over the output.

        Yields:
            int: the next value in the output buffer
        """
        while self._output_buffer:
            yield self._output_buffer.popleft()

    @property
    def memory(self) -> dict[int, int]:
        """Provides direct access to the computer's memory.

        Returns:
            dict[int, int]: the computer's memory, mapped address to value
        """
        return self._memory

    @property
    def terminated(self) -> bool:
        """Program termination flag.

        Returns:
            bool: True after program has terminated, otherwise false
        """
        return self._terminated

    def execute(
        self,
        sleep_after_output: bool = False,
        sleep_when_waiting_for_input: bool = False,
    ) -> bool:
        """Execute the program.

        Args:
            sleep_after_output (bool): if True, returns after an output is generated.
            sleep_when_waiting_for_input (bool): if True, return when waiting for input.

        Returns:
            bool: True if output is generated, else false
        """
        result = False

        # define the instructions
        instructions: dict[int, tuple[int, Callable[[list[int]], int], Action]] = {
            1: (3, lambda p: p[0] + p[1], Action.write),
            2: (3, lambda p: p[0] * p[1], Action.write),
            3: (1, lambda _: self._input_buffer.popleft(), Action.write),
            4: (1, lambda p: p[0], Action.output),
            5: (2, lambda p: p[1] if p[0] != 0 else self._pointer + 3, Action.jump),
            6: (2, lambda p: p[1] if p[0] == 0 else self._pointer + 3, Action.jump),
            7: (3, lambda p: 1 if p[0] < p[1] else 0, Action.write),
            8: (3, lambda p: 1 if p[0] == p[1] else 0, Action.write),
            9: (1, lambda p: p[0], Action.adjust_relative_base),
            99: (0, lambda _: 0, Action.terminate),
        }

        # execute the program
        while True:
            # decode the opcode and parameters
            opcode = self._memory[self._pointer] % 100
            length, operator, action = instructions[opcode]
            modes = [
                ((self._memory[self._pointer] // (10**x)) % 10)
                for x in range(2, 2 + length)
            ]
            params = [
                self._memory[self._memory[self._pointer + j + 1]]
                if modes[j] == 0
                else (
                    self._memory[self._pointer + j + 1]
                    if modes[j] == 1
                    else self._memory[
                        self._memory[self._pointer + j + 1] + self._relative_base
                    ]
                )
                for j in range(length)
            ]

            # check for input, and sleep if required
            if opcode == 3 and not self._input_buffer and sleep_when_waiting_for_input:
                break

            # execute the instruction
            value = operator(params)
            if action == Action.write:
                if modes[-1] == 2:
                    self._memory[
                        self._memory[self._pointer + length] + self._relative_base
                    ] = value
                else:
                    self._memory[self._memory[self._pointer + length]] = value
                self._pointer += length + 1
            elif action == Action.output:
                self._output_buffer.append(value)
                self._pointer += length + 1
                result = True
                if sleep_after_output:
                    break
            elif action == Action.jump:
                self._pointer = value
            elif action == Action.adjust_relative_base:
                self._relative_base += value
                self._pointer += length + 1
            elif action == Action.terminate:
                self._terminated = True
                break
        return result
