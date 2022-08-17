"""Solves the puzzle for Day 12 of Advent of Code 2016.

Leonardo's Monorail

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/12
"""
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


@dataclass
class Instruction:
    """Represents an instruction in the program."""

    action: Action
    first: str
    second: str


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 12
    TITLE = "Leonardo's Monorail"

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

        # parse the input
        self.program = []
        action_map = {
            "cpy": Action.COPY,
            "inc": Action.INCREMENT,
            "dec": Action.DECREMENT,
            "jnz": Action.JUMP,
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
        return self._run()

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(c=1)

    def _run(self, **kwargs: int) -> int:
        # zero all registers
        reg = {k: 0 for k in "abcd"}

        # update registers with key word arguments
        reg.update(kwargs)

        # add all int literals as special registers
        for instruction in self.program:
            items = [instruction.first, instruction.second]
            for item in items:
                if item is not None and (
                    item.isdigit() or (item[0] == "-" and item[1:].isdigit())
                ):
                    reg[item] = int(item)

        i = 0
        while 0 <= i < len(self.program):
            if self.program[i].action == Action.COPY:
                reg[self.program[i].second] = reg[self.program[i].first]
            elif self.program[i].action == Action.INCREMENT:
                reg[self.program[i].first] += 1
            elif self.program[i].action == Action.DECREMENT:
                reg[self.program[i].first] -= 1
            elif (
                self.program[i].action == Action.JUMP
                and reg[self.program[i].first] != 0
            ):
                i += int(self.program[i].second) - 1
            i += 1

        return reg["a"]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
