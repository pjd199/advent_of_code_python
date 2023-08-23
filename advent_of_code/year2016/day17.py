"""Solves the puzzle for Day 17 of Advent of Code 2016.

Two Steps Forward

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/17
"""
from collections import deque
from collections.abc import Callable
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
    DAY = 17
    TITLE = "Two Steps Forward"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"[a-z]+", str_processor)
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

        queue = deque([(0, 0, "")])

        moves: dict[str, Callable[[int, int], tuple[int, int]]] = {
            "U": lambda x, y: (x, y - 1),
            "D": lambda x, y: (x, y + 1),
            "L": lambda x, y: (x - 1, y),
            "R": lambda x, y: (x + 1, y),
        }

        # search for the longest and shortest paths using a
        # breadth first search
        self.shortest = " " * 10000
        self.longest = ""
        while queue:
            x, y, path = queue.popleft()

            # check if path has arrived at the destination
            if (x, y) == (3, 3):
                if len(path) < len(self.shortest):
                    self.shortest = path
                if len(path) > len(self.longest):
                    self.longest = path
                continue

            # for all valid moves
            for i, (direction, move) in enumerate(moves.items()):
                new_path = f"{path}{direction}"
                new_x, new_y = move(x, y)
                if (
                    0 <= new_x < 4
                    and 0 <= new_y < 4
                    and md5(
                        f"{self.input}{path}".encode(), usedforsecurity=False
                    ).hexdigest()[i]
                    in "bcdef"
                ):
                    queue.append((new_x, new_y, new_path))

        self.run = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
