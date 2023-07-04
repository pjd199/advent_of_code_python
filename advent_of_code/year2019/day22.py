"""Solves the puzzle for Day 22 of Advent of Code 2019.

Slam Shuffle

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/22
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 22
    TITLE = "Slam Shuffle"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (r"deal into new stack", lambda _: ("stack", 0)),
            (r"cut (-?\d+)", lambda m: ("cut", int(m[1]))),
            (r"deal with increment (\d+)", lambda m: ("increment", int(m[1]))),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        length = 10007
        location = 2019
        for instruction, number in self.input:
            if instruction == "stack":
                location = (-location - 1) % length
            elif instruction == "cut":
                location = (location - number) % length
            else:
                location = (location * number) % length
        return location

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # with help from reddit /u/bla2,
        # using linear functions and Little Fermat's inverse
        n = 119315717514047
        card = 2020

        a, b = 1, 0
        for instruction, number in self.input:
            if instruction == "stack":
                la, lb = -1, -1
            elif instruction == "cut":
                la, lb = 1, -number
            else:
                la, lb = number, 0
            a = (la * a) % n
            b = (la * b + lb) % n

        m = 101741582076661
        ma = pow(a, m, n)
        mb = (b * (ma - 1) * pow(a - 1, n - 2, n)) % n
        return ((card - mb) * pow(ma, n - 2, n)) % n


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
