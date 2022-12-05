"""Solves the puzzle for Day 20 of Advent of Code 2018.

A Regular Map

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/20
"""
from pathlib import Path
from sys import maxsize, path
from typing import Callable, Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 20
    TITLE = "A Regular Map"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"\^[NSEW|()]+\$", str_processor)

        self.rooms = {(0, 0): 0}  # {(x, y) : doors}

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if len(self.rooms) == 1:
            self._solve()

        return max(self.rooms.values())

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if len(self.rooms) == 1:
            self._solve()

        return sum(1 for d in self.rooms.values() if d >= 1000)

    def _solve(self) -> None:
        """Solve the puzzle."""
        moves: Dict[str, Callable[[int, int], Tuple[int, int]]] = {
            "N": lambda x, y: (x, y - 2),
            "S": lambda x, y: (x, y + 2),
            "E": lambda x, y: (x + 2, y),
            "W": lambda x, y: (x - 2, y),
        }

        # use a stack to remember location when traversing branches
        stack = []
        x, y, doors = 0, 0, 0
        for c in self.input[1:-1]:
            if c in "NSEW":
                x, y = moves[c](x, y)
                doors += 1
                self.rooms[(x, y)] = min(self.rooms.get((x, y), maxsize), doors)
            elif c == "(":
                stack.append((x, y, doors))
            elif c == ")":
                x, y, doors = stack.pop()
            elif c == "|":
                x, y, doors = stack[-1]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
