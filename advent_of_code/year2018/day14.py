"""Solves the puzzle for Day 14 of Advent of Code 2018.

Chocolate Charts

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/14
"""
from dataclasses import dataclass
from pathlib import Path
from sys import path
from typing import Optional

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Link:
    """A link in linked list."""

    score: int
    previous_link: Optional["Link"] = None
    next_link: Optional["Link"] = None


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 14
    TITLE = "Chocolate Charts"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"\d+", str_processor)

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        scores = [3, 7]
        elf_one = 0
        elf_two = 1

        number = int(self.input)
        while len(scores) <= (number + 10):
            total = scores[elf_one] + scores[elf_two]
            scores.extend([total] if total < 10 else divmod(total, 10))
            elf_one = (elf_one + scores[elf_one] + 1) % len(scores)
            elf_two = (elf_two + scores[elf_two] + 1) % len(scores)

        return "".join(str(score) for score in scores[number : number + 10])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        scores = [3, 7]
        elf_one = 0
        elf_two = 1

        digits = [int(x) for x in self.input]

        while (
            digits != scores[-len(digits) :]
            and digits != scores[(-len(digits) - 1) : -1]
        ):
            total = scores[elf_one] + scores[elf_two]
            scores.extend([total] if total < 10 else divmod(total, 10))
            elf_one = (elf_one + scores[elf_one] + 1) % len(scores)
            elf_two = (elf_two + scores[elf_two] + 1) % len(scores)

        return (
            len(scores) - len(digits) - (0 if scores[-len(digits) :] == digits else 1)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
