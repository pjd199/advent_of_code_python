"""Solution for day 5 of Advent of Code 2015."""
from re import compile
from typing import List

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

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

        self.input = []
        pattern = compile(r"(?P<str>[a-z]+)")
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                self.input.append(match["str"])
            else:
                raise RuntimeError(f"Parse error at line {i+1}: {line}")

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
