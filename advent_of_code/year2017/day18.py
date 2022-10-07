"""Solves the puzzle for Day 18 of Advent of Code 2017.

Duet

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/18
"""
from collections import deque
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Deque, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, enum_re, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class _Operation(Enum):
    SEND = "snd"
    SET = "set"
    ADD = "add"
    MULTIPLY = "mul"
    MODULUS = "mod"
    RECIEVE = "rcv"
    JUMP = "jgz"


@dataclass
class _Instruction:
    op: _Operation
    left: str
    right: str = ""


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 18
    TITLE = "Duet"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                rf"(?P<op>{enum_re(_Operation)}) "
                r"(?P<left>[a-z\-0-9]+) ?(?P<right>[a-z\-0-9]+)?",
                dataclass_processor(_Instruction),
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        reg = {x.left: 0 for x in self.input}
        numeric_patch = {
            x.right: int(x.right) for x in self.input if x.right.strip("-").isnumeric()
        }
        reg.update(numeric_patch)

        played = -1

        i = 0
        while 0 <= i < len(self.input):
            op, left, right = self.input[i].op, self.input[i].left, self.input[i].right
            if op == _Operation.SEND:
                played = reg[left]
                i += 1
            elif op == _Operation.SET:
                reg[left] = reg[right]
                i += 1
            elif op == _Operation.ADD:
                reg[left] += reg[right]
                i += 1
            elif op == _Operation.MULTIPLY:
                reg[left] *= reg[right]
                i += 1
            elif op == _Operation.MODULUS:
                reg[left] %= reg[right]
                i += 1
            elif op == _Operation.RECIEVE and reg[left] != 0:
                break
            elif op == _Operation.JUMP and reg[left] > 0:
                i += reg[right]
            else:
                i += 1

        return played

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # initialise the registers
        reg = [{x.left: 0 for x in self.input}, {x.left: 0 for x in self.input}]
        numeric_patch = {
            x.right: int(x.right) for x in self.input if x.right.strip("-").isnumeric()
        }
        reg[0].update(numeric_patch)
        reg[1].update(numeric_patch)
        reg[0]["p"] = 0
        reg[1]["p"] = 1

        send_count = [0, 0]
        queue: List[Deque[int]] = [deque(), deque()]
        waiting = [False, False]
        alive = [True, True]

        turn = 0
        i = [0, 0]
        while any(x for x in alive) and not all(x for x in waiting):
            instruction = self.input[i[turn]]

            if instruction.op == _Operation.SEND:
                send_count[turn] += 1
                queue[(turn + 1) % 2].append(reg[turn][instruction.left])
                waiting[(turn + 1) % 2] = False
                i[turn] += 1

            elif instruction.op == _Operation.RECIEVE:
                if queue[turn]:
                    reg[turn][instruction.left] = queue[turn].popleft()
                    waiting[turn] = False
                    i[turn] += 1
                else:
                    waiting[turn] = True

            elif instruction.op == _Operation.SET:
                reg[turn][instruction.left] = reg[turn][instruction.right]
                i[turn] += 1

            elif instruction.op == _Operation.ADD:
                reg[turn][instruction.left] += reg[turn][instruction.right]
                i[turn] += 1

            elif instruction.op == _Operation.MULTIPLY:
                reg[turn][instruction.left] *= reg[turn][instruction.right]
                i[turn] += 1

            elif instruction.op == _Operation.MODULUS:
                reg[turn][instruction.left] %= reg[turn][instruction.right]
                i[turn] += 1

            else:  # op == _Operation.JUMP:
                if reg[turn][instruction.left] > 0:
                    i[turn] += reg[turn][instruction.right]
                else:
                    i[turn] += 1

            turn = (turn + 1) % 2

        return send_count[1]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
