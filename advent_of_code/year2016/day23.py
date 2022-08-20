"""Solves the puzzle for Day 23 of Advent of Code 2016.

Safe Cracking

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/23
"""
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Action(Enum):
    """Enum representing the actions."""

    COPY = auto()
    INCREMENT = auto()
    DECREMENT = auto()
    JUMP = auto()
    TOGGLE = auto()
    MULTIPLY = auto()
    NOOP = auto()


@dataclass
class Instruction:
    """Represents an instruction in the program."""

    action: Action
    first: str
    second: str


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 23
    TITLE = "Safe Cracking"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        #         puzzle_input = """cpy 2 a
        # tgl a
        # tgl a
        # tgl a
        # cpy 1 a
        # dec a
        # dec a""".splitlines()

        # parse the input
        self.program = []
        action_map = {
            "cpy": Action.COPY,
            "inc": Action.INCREMENT,
            "dec": Action.DECREMENT,
            "jnz": Action.JUMP,
            "tgl": Action.TOGGLE,
        }
        pattern = compile(
            rf"(?P<action>({'|'.join(action_map.keys())})) "
            rf"(?P<first>(-?\d+|[abcd]))\s?"
            rf"(?P<second>(-?\d+|[abcd]))?"
        )
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.program.append(
                    Instruction(action_map[m["action"]], m["first"], m["second"])
                )
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(self.program, a=7)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # run with loop optimisation
        return self._run(
            self.program[:4]
            + [
                Instruction(Action.COPY, "1", "a"),
                Instruction(Action.MULTIPLY, "a", "b"),
                Instruction(Action.MULTIPLY, "a", "d"),
                Instruction(Action.COPY, "0", "c"),
                Instruction(Action.COPY, "0", "d"),
                Instruction(Action.NOOP, "0", "0"),
            ]
            + self.program[10:],
            a=12,
        )

    def _run(self, program: List[Instruction], **kwargs: int) -> int:
        # work on a copy of the program, so we can modify instructions
        program = deepcopy(program)

        # zero all registers
        reg = {k: 0 for k in "abcd"}

        # update registers with key word arguments
        reg.update(kwargs)

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
        toggle_map = {
            Action.COPY: Action.JUMP,
            Action.INCREMENT: Action.DECREMENT,
            Action.DECREMENT: Action.INCREMENT,
            Action.JUMP: Action.COPY,
            Action.TOGGLE: Action.INCREMENT,
        }
        i = 0
        while 0 <= i < len(program):
            if program[i].action == Action.COPY and not program[i].second.isdigit():
                reg[program[i].second] = reg[program[i].first]

            elif program[i].action == Action.INCREMENT:
                reg[program[i].first] += 1

            elif program[i].action == Action.DECREMENT:
                reg[program[i].first] -= 1

            elif program[i].action == Action.JUMP and reg[program[i].first] != 0:
                i += reg[program[i].second] - 1

            elif program[i].action == Action.TOGGLE and 0 <= i + reg[
                program[i].first
            ] < len(program):
                program[i + reg[program[i].first]].action = toggle_map[
                    program[i + reg[program[i].first]].action
                ]

            elif program[i].action == Action.MULTIPLY:
                reg[program[i].first] *= reg[program[i].second]

            i += 1

        return reg["a"]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
