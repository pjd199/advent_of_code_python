"""Solves the puzzle for Day 9 of Advent of Code 2017.

Stream Processing

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/9
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 9
    TITLE = "Stream Processing"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"[{}<>!'\",a-z]+", str_processor)
        self.total_score = -1
        self.total_garbage = -1

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if self.total_score == -1:
            self._solve()
        return self.total_score

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if self.total_garbage == -1:
            self._solve()
        return self.total_garbage

    def _solve(self) -> None:
        """Solve the puzzle."""
        depth = 0
        garbage = False
        ignore_next = False
        self.total_score = 0
        self.total_garbage = 0
        for x in self.input:
            if ignore_next:
                ignore_next = False
            elif x == "!":
                ignore_next = True
            elif x == ">":
                garbage = False
            elif garbage:
                self.total_garbage += 1
            else:
                if x == "<":
                    garbage = True
                if x == "{":
                    depth += 1
                    self.total_score += depth
                elif x == "}":
                    depth -= 1


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
