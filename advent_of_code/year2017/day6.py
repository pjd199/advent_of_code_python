"""Solves the puzzle for Day 6 of Advent of Code 2017.

Memory Reallocation

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/6
"""
from copy import deepcopy
from itertools import count
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 6
    TITLE = "Memory Reallocation"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input,
            r"\d+",
            int_processor,
            delimiter=r"\t",
            max_length=1,
        )[0]
        self.solved = False
        self.loop_found_at = 0
        self.loop_length = 0

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.solved:
            self._solve()

        return self.loop_found_at

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.solved:
            self._solve()

        return self.loop_length

    def _solve(self) -> None:
        """Solve the puzzle."""
        banks = deepcopy(self.input)
        seen = {tuple(banks): 0}

        for cycle in count():
            # find bank with most blocks
            bank = 0
            blocks = banks[0]
            for i, x in enumerate(banks):
                if x > blocks:
                    bank = i
                    blocks = x

            # redistribute the blocks
            banks[bank] = 0
            for i in range(1, blocks + 1):
                banks[(bank + i) % len(banks)] += 1
            cycle += 1

            # check for a loop
            if tuple(banks) in seen:
                self.loop_found_at = cycle
                self.loop_length = cycle - seen[tuple(banks)]
                self.solved = True
                break
            else:
                seen[tuple(banks)] = cycle


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
