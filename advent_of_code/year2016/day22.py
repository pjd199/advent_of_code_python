"""Solves the puzzle for Day 22 of Advent of Code 2016.

Grid Computing

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/22
"""
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Node:
    """Data Class for a node object."""

    x: int
    y: int
    size: int
    used: int
    available: int
    percent: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 22
    TITLE = "Grid Computing"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                r"/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+) *"
                r"(?P<size>\d+)T *(?P<used>\d+)T "
                r"*(?P<available>\d+)T *(?P<percent>\d+)%",
                dataclass_processor(Node),
            ),
            header=(
                "root@ebhq-gridcenter# df -h",
                "Filesystem              Size  Used  Avail  Use%",
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return len(
            [
                (a, b)
                for a, b in permutations(self.input, 2)
                if a.used != 0 and a.used <= b.available
            ]
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # find the special nodes
        empty = min(self.input, key=lambda n: n.used)
        goal = max(self.input, key=lambda n: n.x)
        wall_start = min(
            (node for node in self.input if node.size > 100), key=lambda n: n.x
        )

        # use the formula to move the empty space to front of the goal,
        # move the goal into the empty space, move the empty space to the
        # front of the goal and reapeat until reach destination.
        return (
            empty.y
            + (empty.x - wall_start.x + 1)
            + (goal.x - wall_start.x)
            + 5 * (goal.x - 1)
            + 1
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
