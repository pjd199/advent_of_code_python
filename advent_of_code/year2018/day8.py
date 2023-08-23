"""Solves the puzzle for Day 8 of Advent of Code 2018.

Memory Maneuver

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/8
"""
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class TreeNode:
    """Represent the tree decoded from the input."""

    children: list["TreeNode"] = field(default_factory=list)
    data: list[int] = field(default_factory=list)


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 8
    TITLE = "Memory Maneuver"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input, (r"\d+", int_processor), delimiter=" "
        )
        self.decoded = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.decoded:
            self.root = self._read_node(iter(self.input))
            self.decoded = True

        def sum_data(node: TreeNode) -> int:
            if node.children:
                return sum(node.data) + sum(sum_data(x) for x in node.children)
            return sum(node.data)

        return sum_data(self.root)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.decoded:
            self.root = self._read_node(iter(self.input))
            self.decoded = True

        def sum_data(node: TreeNode) -> int:
            if node.children:
                return sum(
                    sum_data(node.children[x - 1])
                    for x in node.data
                    if 0 < x <= len(node.children)
                )
            return sum(node.data)

        return sum_data(self.root)

    def _read_node(self, itr: Iterator[int]) -> TreeNode:
        children = next(itr)
        length = next(itr)
        return TreeNode(
            [self._read_node(itr) for _ in range(children)],
            [next(itr) for _ in range(length)],
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
