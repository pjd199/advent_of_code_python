"""Solves the puzzle for Day 21 of Advent of Code 2016.

Scrambled Letters and Hash

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/21
"""
from enum import Enum, auto
from pathlib import Path
from re import compile
from sys import path
from typing import Callable, Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Direction(Enum):
    """Which way? Left or Right."""

    LEFT = auto()
    RIGHT = auto()


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 21
    TITLE = "Scrambled Letters and Hash"

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

        # parse the input
        self.operations = []
        pattern = compile(
            r"(?P<action>"
            r"(swap position|swap letter|rotate (left|right|based on)|reverse|move)) "
            r"((?P<first_index>\d+) with position (?P<second_index>\d+)"
            r"|(?P<first_letter>[a-z]) with letter (?P<second_letter>[a-z])"
            r"|(?P<steps>\d+) steps?"
            r"|position of letter (?P<letter>[a-z])"
            r"|positions (?P<start>\d+) through (?P<end>\d+)"
            r"|position (?P<move_from>\d+) to position (?P<move_to>\d+))"
        )
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.operations.append(
                    {
                        k: int(v) if v.isnumeric() else v
                        for k, v in m.groupdict().items()
                        if v
                    }
                )
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i + 1}")

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        self.password = list("abcdefgh")

        functions: Dict[str, Callable[..., None]] = {
            "swap position": self._swap_posistions,
            "swap letter": self._swap_letter,
            "reverse": self._reverse,
            "rotate left": self._rotate_left,
            "rotate right": self._rotate_right,
            "rotate based on": self._rotate_based_on,
            "move": self._move,
        }
        for operation in self.operations:
            functions[str(operation["action"])](
                **{k: v for k, v in operation.items() if k != "action"}
            )

        return "".join(self.password)

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        self.password = list("fbgdceah")
        functions: Dict[str, Callable[..., None]] = {
            "swap position": self._swap_posistions,
            "swap letter": self._swap_letter,
            "reverse": self._reverse,
            "rotate left": self._rotate_right,
            "rotate right": self._rotate_left,
            "rotate based on": self._reverse_rotate_based_on,
            "move": self._reverse_move,
        }
        log = []
        log.append(self.password.copy())
        for operation in reversed(self.operations):
            functions[str(operation["action"])](
                **{k: v for k, v in operation.items() if k != "action"}
            )
            log.append(self.password.copy())

        return "".join(self.password)

    def _rotate(self, data: List[str], steps: int, direciton: Direction) -> List[str]:
        """Rotate a list, left or right.

        Args:
            data (List[str]): the input list
            steps (int): number of steps to rotate
            direciton (Direction): the directin, left or right

        Returns:
            List[str]: _description_
        """
        if direciton == Direction.RIGHT:
            steps = -steps
        return [data[(i + steps) % len(data)] for i in range(len(data))]

    def _swap_posistions(self, first_index: int, second_index: int) -> None:
        """Swap positions of two indexes.

        Args:
            first_index (int): the first position
            second_index (int): the second position
        """
        self.password[first_index], self.password[second_index] = (
            self.password[second_index],
            self.password[first_index],
        )

    def _swap_letter(self, first_letter: str, second_letter: str) -> None:
        """Swap two letters in the password.

        Args:
            first_letter (str): the first letter to find
            second_letter (str): the second letter to find
        """
        i = self.password.index(first_letter)
        j = self.password.index(second_letter)
        self.password[i], self.password[j] = self.password[j], self.password[i]

    def _rotate_left(self, steps: int) -> None:
        """Rotate the password to the left.

        Args:
            steps (int): the number of steps to rotate
        """
        self.password = self._rotate(self.password, steps, Direction.LEFT)

    def _rotate_right(self, steps: int) -> None:
        """Rotate to the right.

        Args:
            steps (int): the number of steps to rotate
        """
        self.password = self._rotate(self.password, steps, Direction.RIGHT)

    def _rotate_based_on(self, letter: str) -> None:
        """Rotate based on the location of the letter.

        Args:
            letter (str): the letter to use as rotation index
        """
        steps = self.password.index(letter)
        steps += 2 if steps >= 4 else 1
        self.password = self._rotate(self.password, steps, Direction.RIGHT)

    def _reverse_rotate_based_on(self, letter: str) -> None:
        """Find the reverse of rotate based on.

        Args:
            letter (str): the letter to use as rotation index
        """
        for i in range(len(self.password)):
            prev = self._rotate(self.password, i, Direction.LEFT)
            steps = prev.index(letter)
            steps += 2 if steps >= 4 else 1
            if self.password == self._rotate(prev, steps, Direction.RIGHT):
                self.password = prev
                break

    def _reverse(self, start: int, end: int) -> None:
        """Reverse the given range in the password.

        Args:
            start (int): the start of the section
            end (int): the end of the section
        """
        self.password[start : end + 1] = reversed(self.password[start : end + 1])

    def _move(self, move_from: int, move_to: int) -> None:
        """Reverse the given range.

        Args:
            move_from (int): the index to remove from
            move_to (int): the index to insert to
        """
        self.password.insert(move_to, self.password.pop(move_from))

    def _reverse_move(self, move_from: int, move_to: int) -> None:
        """Reverse of the move function.

        Args:
            move_from (int): the index to remove from
            move_to (int): the index to insert to
        """
        self.password.insert(move_from, self.password.pop(move_to))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
