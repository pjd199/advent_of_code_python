"""Solves the puzzle for Day 14 of Advent of Code 2016.

One-Time Pad

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/14
"""
from collections import defaultdict
from hashlib import md5
from itertools import count
from pathlib import Path
from re import compile
from sys import path
from typing import Generator, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


def stretch_digest(x: str) -> str:  # pragma: no cover
    """Calculate the stretch digest of the input.

    Args:
        x (str): the input

    Returns:
        str: the stretch digest
    """
    for _ in range(2017):
        x = md5(x.encode()).hexdigest()  # nosec
    return x


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 14
    TITLE = "One-Time Pad"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"\w+", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._find(
            (md5(f"{self.input}{j}".encode()).hexdigest() for j in count()),  # nosec
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle, with multiprocessing speed boost.

        Returns:
            int: the answer
        """
        return self._find(
            iter((stretch_digest(f"{self.input}{j}") for j in range(25000)))
        )

    def _find(self, iterator: Generator[str, None, None]) -> int:
        """Search for the answers.

        Args:
            iterator (Generator[str, None, None]): the iterator for the MD5 hash stream

        Returns:
            int: the index after 64 successful 5* hashes
        """
        list_of_threes = defaultdict(list)
        pattern_three = compile(r"(.)\1\1")
        pattern_five = compile(r"(.)\1\1\1\1")

        found = 0
        result = -1
        i = -1

        while found < 64:
            i += 1
            digest = next(iterator)

            # check for three repeated characters
            if m := pattern_three.search(digest):
                list_of_threes[m[1]].append(i)

            # check for five repeated characters
            if m := pattern_five.search(digest):
                threes = [x for x in list_of_threes[m[1]] if (i - 1000) < x < i]
                for j in threes:
                    found += 1
                    if found == 64:
                        result = j
                        break
        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
