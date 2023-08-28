"""Solves the puzzle for Day 5 of Advent of Code 2016.

How About a Nice Game of Chess?

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from collections.abc import Iterator
from hashlib import md5
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 5
    TITLE = "How About a Nice Game of Chess?"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"(?P<id>[a-z]+)", str_processor)

        # setup the empty cache to help shortcut solving part two if called
        # after part one
        self.cache: dict[int, str] = {}

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        password = []
        for digest in self._digests():
            password.append(digest[5])
            if len(password) == 8:
                break

        return "".join(password)

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        password = [""] * 8
        for digest in self._digests():
            index = int(digest[5], 16)
            if index < len(password) and password[index] == "":
                password[index] = digest[6]
                if password.count("") == 0:
                    break

        return "".join(password)

    def _digests(self) -> Iterator[str]:
        """An iterator for MD5 digests.

        Yields:
            str: The next digest in the stream
        """
        i = 0

        # start with cached digests
        for k, v in sorted(self.cache.items()):
            yield v
            i = k

        # find new digests
        while True:
            # python 3.9 introduced usedforsecurity=False for MD5 function,
            # which raises a security issue for bandit - # nosec is used
            # to ignore this, as there are no security issues here
            digest = md5(
                (self.input + str(i)).encode(), usedforsecurity=False
            ).hexdigest()

            if digest.startswith("00000"):
                self.cache[i] = digest
                yield digest
            i += 1


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
