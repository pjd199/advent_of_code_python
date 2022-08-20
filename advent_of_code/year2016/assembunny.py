"""assembunny definitions and functions required for days 12, 23 & 25."""
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from re import compile
from typing import Iterator, List, Tuple


class Action(Enum):
    """Enum representing the actions."""

    COPY = auto()
    INCREMENT = auto()
    DECREMENT = auto()
    JUMP = auto()
    TOGGLE = auto()
    MULTIPLY = auto()
    NOP = auto()
    OUT = auto()


@dataclass
class Instruction:
    """Represents an instruction in the program."""

    action: Action
    first: str
    second: str

    def astuple(self) -> Tuple[Action, str, str]:
        """Convert the Instruction into a Tuple.

        Returns:
            Tuple[Action, str, str]: the Instruction as a Tuple
        """
        return (self.action, self.first, self.second)


def load(puzzle_input: List[str]) -> List[Instruction]:
    """Load assumbunny from the puzzle input.

    Args:
        puzzle_input (List[str]): the input

    Raises:
        RuntimeError: Raised on a parse error

    Returns:
        List[Instruction]: the loaded program
    """
    action_map = {
        "cpy": Action.COPY,
        "inc": Action.INCREMENT,
        "dec": Action.DECREMENT,
        "jnz": Action.JUMP,
        "tgl": Action.TOGGLE,
        "mul": Action.MULTIPLY,
        "nop": Action.NOP,
        "out": Action.OUT,
    }
    pattern = compile(
        rf"(?P<action>({'|'.join(action_map.keys())})) "
        rf"(?P<first>(-?\d+|[abcd]))\s?"
        rf"(?P<second>(-?\d+|[abcd]))?"
    )

    program = []
    for i, line in enumerate(puzzle_input):
        if m := pattern.fullmatch(line):
            program.append(
                Instruction(action_map[m["action"]], m["first"], m["second"])
            )
        else:
            raise RuntimeError(f"Unable to parse {line} on line {i + 1}")
    return program


def run(
    program: List[Instruction],
    a: int = 0,
    b: int = 0,
    c: int = 0,
    d: int = 0,
) -> int:
    """Run the simulation.

    Args:
        program (List[Instruction]): the program to run
        a (int): initial value for register a. Default 0.
        b (int): initial value for register b. Default 0.
        c (int): initial value for register c. Default 0.
        d (int): initial value for register d. Default 0.

    Returns:
        int: value of register after execution
    """
    return list(run_iter(program, a, b, c, d))[-1]


def run_iter(
    program: List[Instruction],
    a: int = 0,
    b: int = 0,
    c: int = 0,
    d: int = 0,
) -> Iterator[int]:
    """Run the simulation.

    Args:
        program (List[Instruction]): the program to run
        a (int): initial value for register a. Default 0.
        b (int): initial value for register b. Default 0.
        c (int): initial value for register c. Default 0.
        d (int): initial value for register d. Default 0.

    Yields:
        Iterator[int]: the output from the out instruction
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
