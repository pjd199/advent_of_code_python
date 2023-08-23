"""Solves the puzzle for Day 7 of Advent of Code 2022.

No Space Left On Device

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/7
"""
from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Dir:
    """A file system directory structure."""

    dirs: dict[str, "Dir"] = field(default_factory=dict)
    files: dict[str, int] = field(default_factory=dict)
    _size: int = -1

    def size(self) -> int:
        """The size of the directory, including sub directories.

        Returns:
            int: the size
        """
        if self._size == -1:
            self._size = sum(x.size() for x in self.dirs.values()) + sum(
                self.files.values()
            )
        return self._size

    def subdirectories(self) -> list["Dir"]:
        """A list of the all the subdirectories in this directory.

        Returns:
            list["Dir"]: A
        """
        return list(self.dirs.values()) + list(
            chain.from_iterable(x.subdirectories() for x in self.dirs.values())
        )


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 7
    TITLE = "No Space Left On Device"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        # parse the input into a tree structure using Dir
        self.root = Dir()
        stack = [self.root]
        parse_lines(
            puzzle_input,
            (r"\$ cd /", lambda _: None),
            (r"\$ cd ([a-z]+)", lambda m: stack.append(stack[-1].dirs[m[1]])),
            (r"\$ cd \.\.", lambda _: stack.pop()),
            (r"\$ ls", lambda _: None),
            (r"dir ([a-z]+)", lambda m: stack[-1].dirs.update({m[1]: Dir()})),
            (r"(\d+) ([a-z\.]+)", lambda m: stack[-1].files.update({m[2]: int(m[1])})),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            x.size()
            for x in [self.root, *self.root.subdirectories()]
            if x.size() <= 100000
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        target = 30000000 - (70000000 - self.root.size())

        return next(
            x.size()
            for x in sorted(
                [self.root, *self.root.subdirectories()], key=lambda x: x.size()
            )
            if x.size() > target
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
