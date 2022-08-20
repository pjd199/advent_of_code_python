"""Solves the puzzle for Day 7 of Advent of Code 2016.

Internet Protocol Version 7

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 7
    TITLE = "Internet Protocol Version 7"

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
        self.input = []
        pattern = compile(r"\w+(\[\w+\]\w+)+")
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.input.append(m[0])
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i + 1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        supernet_pattern = compile(r"(\w+)(?:\[|$)")
        hypernet_pattern = compile(r"\[(\w+)\]")
        return len(
            [
                line
                for line in self.input
                if any(
                    a1 == a2 and b1 == b2 and a1 != b1
                    for token in supernet_pattern.findall(line)
                    for a1, b1, b2, a2 in zip(token, token[1:], token[2:], token[3:])
                )
                and not any(
                    a1 == a2 and b1 == b2 and a1 != b1
                    for token in hypernet_pattern.findall(line)
                    for a1, b1, b2, a2 in zip(token, token[1:], token[2:], token[3:])
                )
            ]
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        supernet_pattern = compile(r"(\w+)(?:\[|$)")
        hypernet_pattern = compile(r"\[(\w+)\]")
        return len(
            [
                line
                for line in self.input
                if (
                    {
                        f"{a1}{b}"
                        for token in supernet_pattern.findall(line)
                        for a1, b, a2 in zip(token, token[1:], token[2:])
                        if a1 == a2 and a1 != b
                    }
                    & {
                        f"{a}{b2}"
                        for token in hypernet_pattern.findall(line)
                        for b1, a, b2 in zip(token, token[1:], token[2:])
                        if b1 == b2 and a != b1
                    }
                )
            ]
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
