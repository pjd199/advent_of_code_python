"""Solves the puzzle for Day 10 of Advent of Code 2018.

The Stars Align

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/10
"""
from dataclasses import dataclass
from itertools import count
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.ocr import ocr_coordinates
from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Star:
    """Represents a star in the puzzle input."""

    position_x: int
    position_y: int
    velocity_x: int
    velocity_y: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 10
    TITLE = "The Stars Align"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        #         puzzle_input = """position=< 9,  1> velocity=< 0,  2>
        # position=< 7,  0> velocity=<-1,  0>
        # position=< 3, -2> velocity=<-1,  1>
        # position=< 6, 10> velocity=<-2, -1>
        # position=< 2, -4> velocity=< 2,  2>
        # position=<-6, 10> velocity=< 2, -2>
        # position=< 1,  8> velocity=< 1, -1>
        # position=< 1,  7> velocity=< 1,  0>
        # position=<-3, 11> velocity=< 1, -2>
        # position=< 7,  6> velocity=<-1, -1>
        # position=<-2,  3> velocity=< 1,  0>
        # position=<-4,  3> velocity=< 2,  0>
        # position=<10, -3> velocity=<-1,  1>
        # position=< 5, 11> velocity=< 1, -2>
        # position=< 4,  7> velocity=< 0, -1>
        # position=< 8, -2> velocity=< 0,  1>
        # position=<15,  0> velocity=<-2,  0>
        # position=< 1,  6> velocity=< 1,  0>
        # position=< 8,  9> velocity=< 0, -1>
        # position=< 3,  3> velocity=<-1,  1>
        # position=< 0,  5> velocity=< 0, -1>
        # position=<-2,  2> velocity=< 2,  0>
        # position=< 5, -2> velocity=< 1,  2>
        # position=< 1,  4> velocity=< 2,  1>
        # position=<-2,  7> velocity=< 2, -2>
        # position=< 3,  6> velocity=<-1, -1>
        # position=< 5,  0> velocity=< 1,  0>
        # position=<-6,  0> velocity=< 2,  0>
        # position=< 5,  9> velocity=< 1, -2>
        # position=<14,  7> velocity=<-2,  0>
        # position=<-3,  6> velocity=< 2, -1>""".splitlines()
        self.input = parse_lines(
            puzzle_input,
            (
                r"position=< *(?P<position_x>-?\d+), *(?P<position_y>-?\d+)> "
                r"velocity=< *(?P<velocity_x>-?\d+), *(?P<velocity_y>-?\d+)>",
                dataclass_processor(Star),
            ),
        )
        self.time = -1
        self.word = ""

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        if not self.word:
            self._solve()

        return self.word

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.word:
            self._solve()

        return self.time

    def _solve(self) -> None:
        """Solve part one of the puzzle."""
        for i in count():
            sky = set()
            for star in self.input:
                sky.add(
                    (
                        star.position_x + (star.velocity_x * i),
                        star.position_y + (star.velocity_y * i),
                    )
                )

            if max(y for _, y in sky) - min(y for _, y in sky) < 10:
                self.word = ocr_coordinates(sky)
                self.time = i
                break


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
