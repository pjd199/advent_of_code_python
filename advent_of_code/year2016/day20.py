"""Solves the puzzle for Day 20 of Advent of Code 2016.

Firewall Rules

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/20
"""
from dataclasses import astuple, dataclass
from pathlib import Path
from sys import path
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 20
    TITLE = "Firewall Rules"

    @dataclass(order=True)
    class _RangeData:
        lower: int
        upper: int

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (r"(?P<lower>\d+)-(?P<upper>\d+)", dataclass_processor(Solver._RangeData)),
        )
        self.blacklist: List[Tuple[int, int]] = []

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return self.blacklist[0][1] + 1

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return 2**32 - sum(x[1] - x[0] + 1 for x in self.blacklist)

    def _run(self) -> None:
        """Run the simulation."""
        if len(self.blacklist) > 0:
            return

        sorted_input = sorted(self.input)
        section_start, section_end = astuple(sorted_input[0])
        for x in sorted_input:
            if x.lower <= section_end or section_end + 1 == x.lower:
                # extend the section
                section_end = max(section_end, x.upper)
            else:
                # end the section, and start a new one
                self.blacklist.append((section_start, section_end))
                section_start, section_end = x.lower, x.upper

        # append the final section
        self.blacklist.append((section_start, section_end))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
