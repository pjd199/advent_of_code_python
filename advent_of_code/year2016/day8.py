"""Solves the puzzle for Day 8 of Advent of Code 2016.

Two-Factor Authentication

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from re import compile
from sys import path
from typing import DefaultDict, List, Tuple

from advent_of_code_ocr import convert_array_6  # type: ignore

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    @dataclass
    class _Instruction:
        pass

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

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        self.input: List[Solver._Instruction] = []
        pattern = compile(
            r"(?:rect (?P<width>\d+)x(?P<height>\d+))"
            r"|(?:rotate row y=(?P<row>\d+) by (?P<right>\d+))"
            r"|(?:rotate column x=(?P<col>\d+) by (?P<down>\d+))"
        )
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                if m["width"] and m["height"]:
                    self.input.append(Solver._Rect(int(m["width"]), int(m["height"])))
                elif m["row"] and m["right"]:
                    self.input.append(Solver._RotateRow(int(m["row"]), int(m["right"])))
                else:
                    self.input.append(
                        Solver._RotateColumn(int(m["col"]), int(m["down"]))
                    )
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i + 1}")

        self.grid: DefaultDict[Tuple[int, int], bool] = defaultdict(bool)
        self.number_of_columns = 50
        self.number_of_rows = 6

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return len([k for k, v in self.grid.items() if v])

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        letters = []
        self._run()

        # run the letters through OCR
        for offset in range(self.number_of_columns // 5):
            letters.append(
                convert_array_6(
                    [
                        [
                            "#" if self.grid[((offset * 5) + x, y)] else "."
                            for x in range(4)
                        ]
                        for y in range(self.number_of_rows)
                    ]
                )
            )

        return "".join(letters)

    def _run(self) -> DefaultDict[Tuple[int, int], bool]:
        """Run the simulation.

        Returns:
            DefaultDict[Tuple[int, int], bool]: the results
        """
        if len(self.grid) > 0:
            return self.grid

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
