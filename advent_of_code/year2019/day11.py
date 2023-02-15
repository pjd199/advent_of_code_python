"""Solves the puzzle for Day 11 of Advent of Code 2019.

Space Police

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/11
"""
from pathlib import Path
from sys import path
from typing import Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.ocr import ocr_coordinates
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 11
    TITLE = "Space Police"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.computer = IntcodeComputer(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return len(self._paint(0))

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        return ocr_coordinates(
            {(x, y) for (x, y), value in self._paint(1).items() if value == 1}
        )

    def _paint(self, initial: int) -> Dict[Tuple[int, int], int]:
        """Run the computer for the painting robot.

        Args:
            initial (int): The color of the inital square

        Returns:
            pixels (Dict[Tuple[int, int], int]): the pixels, which are painted in situ
        """
        self.computer.reset()

        x, y = (0, 0)
        pixels = {(x, y): initial}
        direction = 0  # 0 is north, 1 is east, 2 is south, 3 is west
        while not self.computer.terminated:
            self.computer.input_data(pixels.get((x, y), 0))
            if self.computer.execute(sleep_after_output=True):
                pixels[(x, y)] = self.computer.read_output()
                self.computer.execute(sleep_after_output=True)
                direction = (direction + (1 if self.computer.read_output() else -1)) % 4
                x, y = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)][direction]

        return pixels


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
