"""Solves the puzzle for Day 11 of Advent of Code 2015.

Corporate Policy

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/11
"""
from collections import deque
from pathlib import Path
from re import findall, search
from sys import path
from typing import Deque, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 11
    TITLE = "Corporate Policy"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"[a-z]+", str_processor)

    def solve_all(self) -> List[str]:
        """Solve both parts.

        Returns:
            List[str]: the answers
        """
        first = self._next_password_after(self.input)
        second = self._next_password_after(first)
        return [first, second]

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        return self._next_password_after(self.input)

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        return self._next_password_after(self._next_password_after(self.input))

    def _next_password_after(self, password: str) -> str:
        """Searches for the next password in the sequence.

        Args:
            password (str): the starting password

        Returns:
            str: the result
        """
        found = False
        while not found:
            # increament the password
            next_password: Deque[str] = deque()
            add_one = True
            for i, c in enumerate(reversed(password)):
                if add_one:
                    if c == "z":
                        next_password.appendleft("a")
                        add_one = True
                    elif c in "ilo":
                        # skipping these letters banned by rule two
                        next_password.appendleft(chr(ord(c) + 2))
                        add_one = False
                    else:
                        next_password.appendleft(chr(ord(c) + 1))
                        add_one = False
                else:
                    next_password.appendleft(password[:-i])
                    break
            password = "".join(next_password)

            # does this pass all three tests?
            for a, b, c in zip(password, password[1:], password[2:]):
                if (
                    ord(a) + 1 == ord(b)
                    and ord(b) + 1 == ord(c)  # rule 1
                    and search(r"[i|l|o]", password) is None  # rule 2
                    and len(findall(r"(.)\1", password)) >= 2
                ):  # rule 3
                    found = True

        return password


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
