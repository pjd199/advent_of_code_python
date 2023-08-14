"""Solves the puzzle for Day 12 of Advent of Code 2017.

Digital Plumber

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/12
"""
from collections import deque
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 12
    TITLE = "Digital Plumber"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = dict(
            parse_lines(
                puzzle_input,
                (
                    r"(?P<id>\d+) <-> (?P<payload>(\d+(, )?)+)$",
                    lambda m: (
                        int(m["id"]),
                        [int(x) for x in m["payload"].split(", ")],
                    ),
                ),
            )
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return len(self._find_group(0))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        groups = []
        found = set()

        for i in range(max(self.input.keys()) + 1):
            if i not in found:
                group = self._find_group(i)
                groups.append(group)
                found.update(group)

        return len(groups)

    def _find_group(self, number: int) -> set[int]:
        """Find all the members of the group with the number in.

        Args:
            number (int): the id number

        Returns:
            set[int]: the group
        """
        group = set()
        queue: deque[int] = deque()
        queue.append(int(number))

        while queue:
            next_number = queue.popleft()
            group.add(next_number)
            queue.extend(x for x in self.input[next_number] if x not in group)

        return group


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
