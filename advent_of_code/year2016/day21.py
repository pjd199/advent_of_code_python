"""Solves the puzzle for Day 21 of Advent of Code 2016.

Scrambled Letters and Hash

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/21
"""
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Direction(Enum):
    """Which way? Left or Right."""

    LEFT = "left"
    RIGHT = "right"


class _Operation:
    @abstractmethod
    def forward(self, password: list[str]) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def reverse(self, password: list[str]) -> None:
        pass  # pragma: no cover


@dataclass
class _SwapPosition(_Operation):
    first: int
    second: int

    def forward(self, password: list[str]) -> None:
        """Swap positions of two indexes.

        Args:
            password (list[str]): the password to operation on
        """
        password[self.first], password[self.second] = (
            password[self.second],
            password[self.first],
        )

    def reverse(self, password: list[str]) -> None:
        """Reverse swap positions of two indexes.

        Args:
            password (list[str]): the password to operation on
        """
        self.forward(password)


@dataclass
class _SwapLetter(_Operation):
    first: str
    second: str

    def forward(self, password: list[str]) -> None:
        """Swap two letters in the password.

        Args:
            password (list[str]): the password to operation on
        """
        i = password.index(self.first)
        j = password.index(self.second)
        password[i], password[j] = password[j], password[i]

    def reverse(self, password: list[str]) -> None:
        """Reverse swap two letters in the password.

        Args:
            password (list[str]): the password to operation on
        """
        self.forward(password)


@dataclass
class _Rotate(_Operation):
    direction: Direction
    steps: int

    def forward(self, password: list[str]) -> None:
        """Rotate the password.

        Args:
            password (list[str]): the password to operation on
        """
        password[:] = _rotate_list(password, self.steps, self.direction)

    def reverse(self, password: list[str]) -> None:
        """Revese rotate the password.

        Args:
            password (list[str]): the password to operation on
        """
        password[:] = _rotate_list(
            password,
            self.steps,
            Direction.LEFT if self.direction == Direction.RIGHT else Direction.RIGHT,
        )


@dataclass
class _RotateBasedOn(_Operation):
    letter: str

    def forward(self, password: list[str]) -> None:
        """Rotate based on the location of the letter.

        Args:
            password (list[str]): the password to operation on
        """
        steps = password.index(self.letter)
        steps += 2 if steps >= 4 else 1
        password[:] = _rotate_list(password, steps, Direction.RIGHT)

    def reverse(self, password: list[str]) -> None:
        """Find the reverse of rotate based on.

        Args:
            password (list[str]): the password to operation on
        """
        for i in range(len(password)):
            prev = _rotate_list(password, i, Direction.LEFT)
            steps = prev.index(self.letter)
            steps += 2 if steps >= 4 else 1
            if password == _rotate_list(prev, steps, Direction.RIGHT):
                password[:] = prev
                break


@dataclass
class _Reverse(_Operation):
    start: int
    end: int

    def forward(self, password: list[str]) -> None:
        """Reverse the range start to end (inclusive).

        Args:
            password (list[str]): the password to operation on
        """
        password[self.start : self.end + 1] = reversed(
            password[self.start : self.end + 1]
        )

    def reverse(self, password: list[str]) -> None:
        """Reverse reverse the range start to end (inclusive).

        Args:
            password (list[str]): the password to operation on
        """
        self.forward(password)


@dataclass
class _Move(_Operation):
    move_from: int
    move_to: int

    def forward(self, password: list[str]) -> None:
        """Move letter from move_from to move_to.

        Args:
            password (list[str]): the password to operation on
        """
        password.insert(self.move_to, password.pop(self.move_from))

    def reverse(self, password: list[str]) -> None:
        """Reverse move letter from move_from to move_to.

        Args:
            password (list[str]): the password to operation on
        """
        password.insert(self.move_from, password.pop(self.move_to))


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 21
    TITLE = "Scrambled Letters and Hash"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.operations: list[_Operation] = parse_lines(
            puzzle_input,
            (
                r"swap position (?P<first>\d+) with position (?P<second>\d+)",
                dataclass_processor(_SwapPosition),
            ),
            (
                r"swap letter (?P<first>[a-z]) with letter (?P<second>[a-z])",
                dataclass_processor(_SwapLetter),
            ),
            (
                r"rotate (?P<direction>(left|right)) (?P<steps>\d+) steps?",
                dataclass_processor(_Rotate),
            ),
            (
                r"rotate based on position of letter (?P<letter>[a-z])",
                dataclass_processor(_RotateBasedOn),
            ),
            (
                r"reverse positions (?P<start>\d+) through (?P<end>\d+)",
                dataclass_processor(_Reverse),
            ),
            (
                r"move position (?P<move_from>\d+) to position (?P<move_to>\d+)",
                dataclass_processor(_Move),
            ),
        )

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        password = list("abcdefgh")

        for operation in self.operations:
            operation.forward(password)

        return "".join(password)

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        password = list("fbgdceah")

        for operation in reversed(self.operations):
            operation.reverse(password)

        return "".join(password)


def _rotate_list(data: list[str], steps: int, direciton: Direction) -> list[str]:
    """Rotate a list, left or right.

    Args:
        data (list[str]): the input list
        steps (int): number of steps to rotate
        direciton (Direction): the directin, left or right

    Returns:
        list[str]: _description_
    """
    if direciton == Direction.RIGHT:
        steps = -steps
    return [data[(i + steps) % len(data)] for i in range(len(data))]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
