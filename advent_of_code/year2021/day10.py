"""Solves the puzzle for Day 10 of Advent of Code 2021.

Syntax Scoring

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/10
"""
from collections import Counter, deque
from functools import reduce
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 10
    TITLE = "Syntax Scoring"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[\[\]\(\)\{\}<>]+", str_processor))
        self.corrupt: set[str] = set()

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        counter: Counter[str] = Counter()
        expected = {"(": ")", "[": "]", "{": "}", "<": ">"}
        for line in self.input:
            stack: deque[str] = deque()
            for x in line:
                if x in expected:
                    stack.append(x)
                else:
                    if x != expected[stack.pop()]:
                        self.corrupt.add(line)
                        counter.update(x)
                        break
        return (
            counter[")"] * 3
            + counter["]"] * 57
            + counter["}"] * 1197
            + counter[">"] * 25137
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.corrupt:
            self.solve_part_one()
        incomplete_lines = [x for x in self.input if x not in self.corrupt]

        points = {"(": 1, "[": 2, "{": 3, "<": 4}
        scores: list[int] = []
        for line in incomplete_lines:
            stack: deque[int] = deque()
            for x in line:
                if x in points:
                    stack.append(points[x])
                else:
                    stack.pop()
            scores.append(reduce(lambda x, y: (x * 5) + y, reversed(list(stack)), 0))
        scores.sort()
        return scores[len(scores) // 2]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
