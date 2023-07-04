"""Solves the puzzle for Day 18 of Advent of Code 2021.

Snailfish

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/18
"""
from itertools import permutations
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface

OPEN = -1
CLOSE = -2


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 18
    TITLE = "Snailfish"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[\[\]0-9,]+", str_processor))
        self.snailfish: list[list[int]] = []

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._parse_snailfish()
        a = self.snailfish[0]
        for b in self.snailfish[1:]:
            a = self._addition(a, b)
        return self._magnitude(a)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._parse_snailfish()
        return max(
            self._magnitude(self._addition(a, b))
            for a, b in permutations(self.snailfish, 2)
        )

    def _parse_snailfish(self) -> None:
        """Parse the input numbers into a list of numbers."""
        if self.snailfish:
            return

        # encode the snailfish number string, using the int constants
        # OPEN and CLOSE to represent the brackets to avoid a list of mixed
        # int and str
        self.snailfish = [
            [
                int(x) if x.isnumeric() else (OPEN if x == "[" else CLOSE)
                for x in line
                if x != ","
            ]
            for line in self.input
        ]

    def _addition(self, a: list[int], b: list[int]) -> list[int]:
        """Caclulates the addition of a + b in snailfish numbers.

        Args:
            a (list[int]): left operand
            b (list[int]): right operand

        Returns:
            list[int]: the reduced result
        """
        number = [OPEN] + a + b + [CLOSE]
        action = True
        while action:
            while action := self._explode(number):
                pass
            action = self._split(number)
        return number

    def _explode(self, number: list[int]) -> bool:
        """Explode a snailfish number.

        Args:
            number (list[int]): the number

        Returns:
            bool: True if changed, else False
        """
        depth = 0
        for i, x in enumerate(number):
            if x == OPEN:
                depth += 1
            elif x == CLOSE:
                depth -= 1
            elif depth > 4:
                # explode to left
                for j in range(i - 1, 0, -1):
                    if number[j] not in (OPEN, CLOSE):
                        number[j] += number[i]
                        break
                # explode to right
                for j in range(i + 3, len(number), 1):
                    if number[j] not in (OPEN, CLOSE):
                        number[j] += number[i + 1]
                        break
                number[i - 1 : i + 3] = [0]
                return True
        return False

    def _split(self, number: list[int]) -> bool:
        """Split a snailfish number.

        Args:
            number (list[int]): then number

        Returns:
            bool: True is changed, else False.
        """
        for i, x in enumerate(number):
            if number[i] not in (OPEN, CLOSE) and x >= 10:
                left = x // 2
                right = x - left
                number[i : i + 1] = [OPEN, left, right, CLOSE]
                return True
        return False

    def _magnitude(self, number: list[int]) -> int:
        """Calculate the magnitude of the snailfish number.

        Args:
            number (list[int]): the number

        Returns:
            int: the magnitude
        """
        while len(number) > 1:
            i = 0
            while i < len(number) - 3:
                if (
                    number[i] == OPEN
                    and number[i + 1] not in (OPEN, CLOSE)
                    and number[i + 2] not in (OPEN, CLOSE)
                    and number[i + 3] == CLOSE
                ):
                    number[i : i + 4] = [(number[i + 1] * 3) + (number[i + 2] * 2)]
                i += 1
        return number[0]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
