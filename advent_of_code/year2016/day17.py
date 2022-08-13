"""Solves the puzzle for Day 17 of Advent of Code 2016.

Two Steps Forward

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/17
"""
from collections import deque
from hashlib import md5
from pathlib import Path
from re import compile
from sys import path
from typing import Deque, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 17
    TITLE = "Two Steps Forward"

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
        pattern = compile(r"[a-z]+")
        for i, line in enumerate(puzzle_input):
            if (m := pattern.fullmatch(line)) and (i == 0):
                self.input = m[0]
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

        self.run = False

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        self._run()
        return self.shortest

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return len(self.longest)

    def _run(self) -> None:
        """Run the simulation."""
        if self.run:
            return

        queue: Deque[Tuple[int, int, str]] = deque([(0, 0, "")])

        moves = {
            "U": (0, -1),
            "D": (0, +1),
            "L": (-1, 0),
            "R": (+1, 0),
        }

        shortest = " " * 10000
        longest = ""
        while queue:
            x, y, path = queue.popleft()

            if (x, y) == (3, 3):
                if len(path) < len(shortest):
                    shortest = path
                if len(path) > len(longest):
                    longest = path
                continue

            for i, (direction, move) in enumerate(moves.items()):
                new_path = f"{path}{direction}"
                new_x, new_y = x + move[0], y + move[1]
                if (
                    0 <= new_x < 4
                    and 0 <= new_y < 4
                    and md5(f"{self.input}{path}".encode()).hexdigest()[i]  # nosec
                    in "bcdef"
                ):
                    queue.append((new_x, new_y, new_path))

        self.shortest = shortest
        self.longest = longest
        self.run = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)