"""Solves the puzzle for Day 24 of Advent of Code 2017.

Electromagnetic Moat

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/24
"""
from collections import defaultdict
from pathlib import Path
from sys import path
from typing import List, Set, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 24
    TITLE = "Electromagnetic Moat"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"(\d+)/(\d+)", int_tuple_processor))

        self.lookup = defaultdict(list)
        for a, b in self.input:
            self.lookup[a].append(b)
            self.lookup[b].append(a)

        self.strongest = 0
        self.longest_length = 0
        self.longest_strength = 0

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if self.strongest == 0:
            self._solve(0, set())

        return self.strongest

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if self.longest_strength == 0:
            self._solve(0, set())

        return self.longest_strength

    def _solve(self, a: int, bridge: Set[Tuple[int, int]]) -> None:
        """Recusively solve the puzzle.

        Args:
            a (int): the "a" connector
            bridge (Set[Tuple[int, int]]): the bridge so far
        """
        end = True
        for b in self.lookup[a]:
            if not ((a, b) in bridge or (b, a) in bridge):
                end = False
                self._solve(b, bridge | {(a, b)})

        if end:
            strength = sum(a + b for a, b in bridge)
            length = len(bridge)

            if strength > self.strongest:
                self.strongest = strength

            if length > self.longest_length or (
                length == self.longest_length and strength > self.longest_strength
            ):
                self.longest_strength = strength
                self.longest_length = length


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
