"""assembunny definitions and functions required for days 12, 23 & 25."""
from collections.abc import Generator
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, unique

from advent_of_code.utils.parser import dataclass_processor, parse_lines


@unique
class Action(Enum):
    """Enum representing the actions."""

    COPY = "cpy"
    INCREMENT = "inc"
    DECREMENT = "dec"
    JUMP = "jnz"
    TOGGLE = "tgl"
    MULTIPLY = "mul"
    NOP = "nop"
    OUT = "out"


@dataclass
class Instruction:
    """Represents an instruction in the program."""

    action: Action
    first: str
    second: str = ""

    def astuple(self) -> tuple[Action, str, str]:
        """Convert the Instruction into a Tuple.

        Returns:
            tuple[Action, str, str]: the Instruction as a Tuple
        """
        return (self.action, self.first, self.second)


def load(puzzle_input: list[str]) -> list[Instruction]:
    """Load assumbunny from the puzzle input.

    Args:
        puzzle_input (list[str]): the input

    Returns:
        list[Instruction]: the loaded program
    """
    return parse_lines(
        puzzle_input,
        (
            rf"(?P<action>({'|'.join({x.value for x in Action})})) "
            rf"(?P<first>(-?\d+|[abcd]))\s?"
            rf"(?P<second>(-?\d+|[abcd]))?",
            dataclass_processor(Instruction),
        ),
    )


def run(
    program: list[Instruction],
    a: int = 0,
    b: int = 0,
    c: int = 0,
    d: int = 0,
) -> int:
    """Run the simulation.

    Args:
        program (list[Instruction]): the program to run
        a (int): initial value for register a. Default 0.
        b (int): initial value for register b. Default 0.
        c (int): initial value for register c. Default 0.
        d (int): initial value for register d. Default 0.

    Returns:
        int: value of register after execution
    """
    return next(iter(run_iter(program, a, b, c, d)))


def run_iter(
    program: list[Instruction],
    a: int = 0,
    b: int = 0,
    c: int = 0,
    d: int = 0,
) -> Generator[int, None, None]:
    """Run the simulation.

    Args:
        program (list[Instruction]): the program to run
        a (int): initial value for register a. Default 0.
        b (int): initial value for register b. Default 0.
        c (int): initial value for register c. Default 0.
        d (int): initial value for register d. Default 0.

    Yields:
        Generator[int, None, None]: the output from the out instruction
    """
    # create a copy to preserve the original
    program = deepcopy(program)

    # initialise the registers
    reg = {"a": a, "b": b, "c": c, "d": d}

    # add all int literals as special registers
    reg.update(
        {
            item: int(item)
            for instruction in program
            for item in [instruction.first, instruction.second]
            if item is not None and item.lstrip("-").isdigit()
        }
    )

    # create the toggle map
    toggle = {
        Action.COPY: Action.JUMP,
        Action.INCREMENT: Action.DECREMENT,
        Action.DECREMENT: Action.INCREMENT,
        Action.JUMP: Action.COPY,
        Action.TOGGLE: Action.INCREMENT,
    }

    i = 0
    while 0 <= i < len(program):
        action, first, second = program[i].astuple()

        if action == Action.COPY and not second.isdigit():
            reg[second] = reg[first]

        elif action == Action.INCREMENT:
            reg[first] += 1

        elif action == Action.DECREMENT:
            reg[first] -= 1

        elif action == Action.JUMP and reg[first] != 0:
            i += reg[second] - 1

        elif action == Action.TOGGLE and 0 <= (i + reg[first]) < len(program):
            program[i + reg[first]].action = toggle[program[i + reg[first]].action]

        elif action == Action.MULTIPLY:
            reg[first] *= reg[second]

        elif action == Action.OUT:
            yield reg[first]

        i += 1

    yield reg["a"]
