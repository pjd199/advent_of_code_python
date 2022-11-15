"""Solves the puzzle for Day 8 of Advent of Code 2016.

Two-Factor Authentication

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from sys import path
from typing import DefaultDict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.ocr import convert_coordinates
from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    @dataclass
    class _Instruction:
        """Abstract class for the instructions."""

    @dataclass
    class _Rect(_Instruction):
        width: int
        height: int

    @dataclass
    class _RotateRow(_Instruction):
        row: int
        right_shift: int

    @dataclass
    class _RotateColumn(_Instruction):
        col: int
        down_shift: int

    YEAR = 2016
    DAY = 8
    TITLE = "Two-Factor Authentication"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                r"rect (?P<width>\d+)x(?P<height>\d+)",
                dataclass_processor(Solver._Rect),
            ),
            (
                r"rotate row y=(?P<row>\d+) by (?P<right_shift>\d+)",
                dataclass_processor(Solver._RotateRow),
            ),
            (
                r"rotate column x=(?P<col>\d+) by (?P<down_shift>\d+)",
                dataclass_processor(Solver._RotateColumn),
            ),
        )
        self.grid: DefaultDict[Tuple[int, int], bool] = defaultdict(bool)
        self.number_of_columns = 50
        self.number_of_rows = 6

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.grid:
            self._run()

        return len([k for k, v in self.grid.items() if v])

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        if not self.grid:
            self._run()

        # run the letters through OCR
        return "".join(
            convert_coordinates(
                {coordinate for coordinate, on in self.grid.items() if on}
            )
        )

    def _run(self) -> DefaultDict[Tuple[int, int], bool]:
        """Run the simulation.

        Returns:
            DefaultDict[Tuple[int, int], bool]: the results
        """
        for instruction in self.input:
            if isinstance(instruction, Solver._Rect):
                self.grid.update(
                    {
                        (x, y): True
                        for x in range(instruction.width)
                        for y in range(instruction.height)
                    }
                )
            elif isinstance(instruction, Solver._RotateRow):
                self.grid.update(
                    {
                        (
                            (x + instruction.right_shift) % self.number_of_columns,
                            instruction.row,
                        ): self.grid[(x, instruction.row)]
                        for x in range(self.number_of_columns)
                    }
                )
            elif isinstance(instruction, Solver._RotateColumn):
                self.grid.update(
                    {
                        (
                            instruction.col,
                            (y + instruction.down_shift) % self.number_of_rows,
                        ): self.grid[(instruction.col, y)]
                        for y in range(self.number_of_rows)
                    }
                )
        return self.grid


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
