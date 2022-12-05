"""Solves the puzzle for Day 16 of Advent of Code 2018.

Chronal Classification

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/16
"""
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from sys import path
from typing import Callable, Dict, List, Set, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    dataclass_processor,
    int_tuple_processor,
    parse_lines,
    split_sections,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Instruction:
    """An instruction read from the input."""

    opcode: int
    a: int
    b: int
    c: int


@dataclass
class Sample:
    """A sample read from the input."""

    before: Tuple[int, ...]
    instruction: Instruction
    after: Tuple[int, ...]


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 16
    TITLE = "Chronal Classification"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.samples: List[Sample] = []

        # parse the input into sections
        sections = split_sections(puzzle_input, "", min_length=7)

        # parse the samples section
        self.samples = [
            Sample(before, Instruction(*instruction), after)
            for before, instruction, after in (
                parse_lines(
                    section,
                    (r"Before: \[(\d+), (\d+), (\d+), (\d+)\]", int_tuple_processor),
                    (r"(\d+) (\d+) (\d+) (\d+)", int_tuple_processor),
                    (r"After:  \[(\d+), (\d+), (\d+), (\d+)\]", int_tuple_processor),
                    min_length=3,
                    max_length=3,
                )
                for section in sections[:-1]
            )
        ]

        self.program = parse_lines(
            sections[-1],
            (
                r"(?P<opcode>\d+) (?P<a>\d+) (?P<b>\d+) (?P<c>\d+)",
                dataclass_processor(Instruction),
            ),
        )

        # define the actions
        self.actions: Dict[str, Callable[[Tuple[int, ...], Instruction], int]] = {
            "addr": lambda r, i: r[i.a] + r[i.b],
            "addi": lambda r, i: r[i.a] + i.b,
            "mulr": lambda r, i: r[i.a] * r[i.b],
            "muli": lambda r, i: r[i.a] * i.b,
            "banr": lambda r, i: r[i.a] & r[i.b],
            "bani": lambda r, i: r[i.a] & i.b,
            "borr": lambda r, i: r[i.a] | r[i.b],
            "bori": lambda r, i: r[i.a] | i.b,
            "setr": lambda r, i: r[i.a],
            "seti": lambda r, i: i.a,
            "gtir": lambda r, i: 1 if i.a > r[i.b] else 0,
            "gtri": lambda r, i: 1 if r[i.a] > i.b else 0,
            "gtrr": lambda r, i: 1 if r[i.a] > r[i.b] else 0,
            "eqir": lambda r, i: 1 if i.a == r[i.b] else 0,
            "eqri": lambda r, i: 1 if r[i.a] == i.b else 0,
            "eqrr": lambda r, i: 1 if r[i.a] == r[i.b] else 0,
        }

        self.possibilities: Dict[int, Set[str]] = defaultdict(set)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # get the possibilities
        if not self.possibilities:
            self._find_possibilities()

        # find the number of samples with more than three possibilities
        return sum(
            1
            for sample in self.samples
            if len(self.possibilities[sample.instruction.opcode]) >= 3
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # Get the possible actions for each opcode number
        if not self.possibilities:
            self._find_possibilities()

        # narrow down the possibilities into known mappings
        known: Dict[int, str] = {}
        search = True
        while search:
            search = False
            for k, v in self.possibilities.items():
                if len(v) == 1:
                    search = True
                    known[k] = list(v)[0]
                    for p in self.possibilities.values():
                        if known[k] in p:
                            p.remove(known[k])

        # execute the program
        register = [0, 0, 0, 0]
        for instruction in self.program:
            register[instruction.c] = self.actions[known[instruction.opcode]](
                tuple(register), instruction
            )

        return register[0]

    def _find_possibilities(self) -> None:
        """Find all the possible mappings between opcode numbers and strings."""
        for sample in self.samples:
            for opcode in self.actions.keys():
                outcome = list(sample.before)
                outcome[sample.instruction.c] = self.actions[opcode](
                    sample.before, sample.instruction
                )
                if sample.after == tuple(outcome):
                    self.possibilities[sample.instruction.opcode].add(opcode)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
