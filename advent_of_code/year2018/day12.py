"""Solves the puzzle for Day 12 of Advent of Code 2018.

Subterranean Sustainability

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/12
"""
from pathlib import Path
from sys import path
from typing import Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    parse_single_line,
    str_processor,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 12
    TITLE = "Subterranean Sustainability"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        # parse the lines to validate the file format
        parse_lines(
            puzzle_input,
            (r"initial state: ([\.#]+)", str_processor),
            (r"", str_processor),
            (r"([\.#]+) => ([\.#])", str_processor),
            min_length=3,
        )

        # parse the inital state
        self.initial_state = parse_single_line(
            puzzle_input[0:1], r"initial state: ([\.#]+)", lambda m: m[1]
        )

        # parse the rules
        self.rules: Dict[str, str] = {
            key: value
            for key, value in parse_lines(
                puzzle_input[2:],
                (r"([\.#]+) => ([\.#])", str_tuple_processor),
            )
        }

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(20)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(50000000000)

    def _solve(self, length: int) -> int:
        """Solve the puzzle.

        Args:
            length (int): the total number of cycles to run

        Returns:
            int: the result
        """
        # reduce the computational time for a large number of cycles
        limit = 1000
        cycles = length if length <= limit else limit

        current = self.initial_state
        for _ in range(1, cycles + 1):
            working = "..." + current + "..."
            current = "".join(
                [
                    self.rules.get(working[(i - 2) : (i + 3)], ".")
                    for i in range(2, len(working) - 2)
                ]
            )

        if length <= limit:
            return sum(i - cycles for i, c in enumerate(current) if c == "#")
        else:
            return sum(
                i + length - (2 * cycles) for i, c in enumerate(current) if c == "#"
            )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
