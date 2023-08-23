"""Solves the puzzle for Day 12 of Advent of Code 2021.

Passage Pathing

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/12
"""
from collections import Counter, deque
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 12
    TITLE = "Passage Pathing"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input: dict[str, set[str]] = {}
        parsed = parse_lines(puzzle_input, (r"(\w+)-(\w+)", str_tuple_processor))
        for a, b in parsed:
            self.input.setdefault(a, set()).add(b)
            self.input.setdefault(b, set()).add(a)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(allow_second_visit=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(allow_second_visit=True)

    def _solve(self, allow_second_visit: bool) -> int:
        """Solve the puzzle.

        Args:
            allow_second_visit (bool): visit one lowercase node twice

        Returns:
            int: number of routes discovered
        """
        found = 0
        queue: deque[list[str]] = deque([["start"]])

        while queue:
            path = queue.popleft()

            counter = Counter(path)

            moves = [
                x
                for x in self.input[path[-1]]
                if x != "start"
                and (
                    x.isupper()
                    or x not in counter
                    or (
                        allow_second_visit
                        and all(v == 1 for k, v in counter.items() if k.islower())
                    )
                )
            ]

            for x in moves:
                if x == "end":
                    found += 1
                else:
                    queue.append([*path, x])

        return found


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
