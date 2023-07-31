"""Solves the puzzle for Day 5 of Advent of Code 2015.

Doesn't He Have Intern-Elves For This?

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/5
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 5
    TITLE = "Doesn't He Have Intern-Elves For This?"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[a-z]+", str_processor))

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        count = 0
        for line in self.input:
            # count the vowels
            vowels = len([1 for x in line if x in ("a", "e", "i", "o", "u")])

            # count the pairs
            pairs = len([1 for x, y in zip(line, line[1:]) if x == y])

            # count the disallowed strings
            disallowed = len(
                [
                    1
                    for i in range(len(line))
                    if line[i : i + 2] in ("ab", "cd", "pq", "xy")
                ]
            )

            if (vowels >= 3) and (pairs >= 1) and (disallowed == 0):
                count += 1
        return count

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        count = 0
        for line in self.input:
            pairs = len([1 for x, y in zip(line, line[1:]) if line.count(x + y) >= 2])
            splits = len([1 for x, y in zip(line, line[2:]) if x == y])
            if pairs and splits:
                count += 1
        return count


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
