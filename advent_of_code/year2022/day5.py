"""Solves the puzzle for Day 5 of Advent of Code 2022.

Supply Stacks

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/5
"""
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from string import ascii_uppercase
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    dataclass_processor,
    parse_lines,
    split_sections,
    str_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Move:
    """A move of the crane."""

    count: int
    move_from: int
    move_to: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 5
    TITLE = "Supply Stacks"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        # divide the input into the two sections
        stack_section, moves_section = split_sections(puzzle_input, "", 2)

        # parse the stacks section
        stack_lines = parse_lines(
            stack_section, (r"( +|\[[A-Z]\]|\d+)+", str_processor), min_length=2
        )
        stack_numbers = [int(x) for x in stack_lines[-1].split(" ") if x]

        self.stacks = {
            i: [
                line[((i - 1) * 4) + 1]
                for line in stack_lines[-2::-1]
                if line[((i - 1) * 4) + 1] in ascii_uppercase
            ]
            for i in stack_numbers
        }

        # parse the moves section
        self.moves = parse_lines(
            moves_section,
            (
                r"move (?P<count>\d+) from (?P<move_from>\d+) to (?P<move_to>\d+)",
                dataclass_processor(Move),
            ),
        )

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        stacks = deepcopy(self.stacks)

        for x in self.moves:
            stacks[x.move_to].extend(stacks[x.move_from].pop() for _ in range(x.count))

        return "".join([x[-1] for x in stacks.values()])

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        stacks = deepcopy(self.stacks)

        for x in self.moves:
            stacks[x.move_to].extend(stacks[x.move_from][-x.count :])
            del stacks[x.move_from][-x.count :]

        return "".join([x[-1] for x in stacks.values()])


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
