"""Solves the puzzle for Day 3 of Advent of Code 2017.

Spiral Memory

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/3
"""
from itertools import count
from pathlib import Path
from sys import path
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 3
    TITLE = "Spiral Memory"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"\d+", int_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        x, y = self._locate(self.input)
        return abs(x) + abs(y)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # use a grid to store the results
        grid = {self._locate(1): 1}

        result = -1
        for i in count(2):
            x, y = self._locate(i)
            # add all the surrounding squares, if they exist
            grid[(x, y)] = (
                grid.get((x - 1, y - 1), 0)
                + grid.get((x, y - 1), 0)
                + grid.get((x + 1, y - 1), 0)
                + grid.get((x - 1, y), 0)
                + grid.get((x + 1, y), 0)
                + grid.get((x - 1, y + 1), 0)
                + grid.get((x, y + 1), 0)
                + grid.get((x + 1, y + 1), 0)
            )
            # is this greater than our target?
            if grid[(x, y)] > self.input:
                result = grid[(x, y)]
                break

        return result

    def _locate(self, number: int) -> Tuple[int, int]:
        """Find the x, y cooridinate of the input number in the sequence.

        Args:
            number (int): input number

        Returns:
            Tuple[int, int]: (x, y) co-ordinates
        """
        if number == 1:
            return 0, 0

        # find the spiral layer
        layer = 1
        start = pow(2 * layer - 1, 2) + 1
        end = pow(2 * (layer + 1) - 1, 2)
        while not (start <= number <= end):
            layer += 1
            start = pow(2 * layer - 1, 2) + 1
            end = pow(2 * (layer + 1) - 1, 2)

        # calculate the length of the spiral arms ( = length of side - 1)
        arm = (2 * (layer + 1)) - 2

        # find the numbers on the four corners
        bottom_right = end
        bottom_left = end - arm
        top_left = bottom_left - arm
        top_right = top_left - arm

        # # check which arm the input is on, and find it's co-ordinates
        x, y = 0, 0
        if bottom_left <= number <= bottom_right:
            x = -layer + (number - bottom_left)
            y = layer
        elif top_left <= number <= bottom_left:
            x = -layer
            y = -layer + (number - top_left)
        elif top_right <= number <= top_left:
            x = layer - (number - top_right)
            y = -layer
        else:
            x = layer
            y = -layer + (top_right - number)

        return x, y


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
