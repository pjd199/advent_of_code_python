"""Solves the puzzle for Day 2 of Advent of Code 2020.

Password Philosophy

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/2
"""
from dataclasses import dataclass
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Password:
    """A passord line from the input."""

    first: int
    second: int
    letter: str
    word: str


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 2
    TITLE = "Password Philosophy"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                r"(?P<first>\d+)-(?P<second>\d+) (?P<letter>\w): (?P<word>\w+)",
                dataclass_processor(Password),
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1 for p in self.input if p.first <= p.word.count(p.letter) <= p.second
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            1
            for p in self.input
            if (p.word[p.first - 1] != p.word[p.second - 1])
            and (p.word[p.first - 1] == p.letter or p.word[p.second - 1] == p.letter)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
