"""Solves the puzzle for Day 5 of Advent of Code 2016."""
from hashlib import md5
from re import compile
from typing import Dict, Iterable, List

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

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
            or len(puzzle_input) != 1
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        pattern = compile(r"(?P<id>[a-z]+)")
        if m := pattern.fullmatch(puzzle_input[0]):
            self.input = m["id"]
        else:
            raise RuntimeError(f"Unable to parse {puzzle_input[0]} on line 1")

        # setup the empty cache to help shortcut solving part two if called
        # after part one
        self.cache: Dict[int, str] = {}

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

    def _digests(self) -> Iterable[str]:
        """An iterator for MD5 digests.

        Yields:
            Iterator[Iterable[str]]: The next digest in the stream
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
            digest = md5((self.input + str(i)).encode()).hexdigest()  # nosec

            if digest.startswith("00000"):
                self.cache[i] = digest
                yield digest
            i += 1
