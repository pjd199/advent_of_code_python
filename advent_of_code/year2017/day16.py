"""Solves the puzzle for Day 16 of Advent of Code 2017.

Permutation Promenade

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/16
"""
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class _Move:
    @abstractmethod
    def step(self, dancers: List[str]) -> None:
        """Perform a step in the dance, modifing the dancers list.

        Args:
            dancers (List[str]): the list of dancers
        """


@dataclass
class _Spin(_Move):
    length: int

    def step(self, dancers: List[str]) -> None:
        """Perform a step in the dance, modifing the dancers list.

        Args:
            dancers (List[str]): the list of dancers
        """
        dancers[:] = dancers[-self.length :] + dancers[: -self.length]


@dataclass
class _Exchange(_Move):
    a: int
    b: int

    def step(self, dancers: List[str]) -> None:
        """Perform a step in the dance, modifing the dancers list.

        Args:
            dancers (List[str]): the list of dancers
        """
        dancers[self.a], dancers[self.b] = dancers[self.b], dancers[self.a]


@dataclass
class _Partner(_Move):
    a: str
    b: str

    def step(self, dancers: List[str]) -> None:
        """Perform a step in the dance, modifing the dancers list.

        Args:
            dancers (List[str]): the list of dancers
        """
        index_a = dancers.index(self.a)
        index_b = dancers.index(self.b)
        dancers[index_a], dancers[index_b] = dancers[index_b], dancers[index_a]


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 16
    TITLE = "Permutation Promenade"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input,
            (r"s(?P<length>\d+)", dataclass_processor(_Spin)),
            (r"x(?P<a>\d+)/(?P<b>\d+)", dataclass_processor(_Exchange)),
            (r"p(?P<a>[a-p])/(?P<b>[a-p])", dataclass_processor(_Partner)),
            delimiter=",",
        )

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        return self._dance("abcdefghijklmnop")

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        start = "abcdefghijklmnop"
        # find the length of the cycle
        cycle = 0
        dancers = start
        while True:
            dancers = self._dance(dancers)
            cycle += 1
            if dancers == start:
                break

        for _ in range(1000000000 % cycle):
            dancers = self._dance(dancers)

        return "".join(dancers)

    def _dance(self, starting_positions: str) -> str:
        dancers = list(starting_positions)
        for move in self.input:
            move.step(dancers)

        return "".join(dancers)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
