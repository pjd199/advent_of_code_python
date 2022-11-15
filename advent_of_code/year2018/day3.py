"""Solves the puzzle for Day 3 of Advent of Code 2018.

No Matter How You Slice It

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/3
"""
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from sys import path
from typing import Counter as CounterType
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Claim:
    """Claim class for loading input."""

    identifier: int
    left: int
    top: int
    width: int
    height: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 3
    TITLE = "No Matter How You Slice It"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                r"#(?P<identifier>\d+) @ "
                r"(?P<left>\d+),(?P<top>\d+): "
                r"(?P<width>\d+)x(?P<height>\d+)",
                dataclass_processor(Claim),
            ),
        )
        self.fabric: CounterType[Tuple[int, int]] = Counter()

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.fabric.clear()
        for claim in self.input:
            self.fabric.update(
                {
                    (x, y)
                    for x in range(claim.left, claim.left + claim.width)
                    for y in range(claim.top, claim.top + claim.height)
                }
            )

        return sum(1 for x in self.fabric.values() if x >= 2)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.fabric:
            self.solve_part_one()

        return next(
            claim.identifier
            for claim in self.input
            if all(
                self.fabric[(x, y)] == 1
                for x in range(claim.left, claim.left + claim.width)
                for y in range(claim.top, claim.top + claim.height)
            )
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
