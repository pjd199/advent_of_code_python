"""Solves the puzzle for Day 14 of Advent of Code 2020.

Docking Data

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/14
"""
from math import pow
from pathlib import Path
from sys import path
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    int_tuple_processor,
    parse_lines,
    str_processor_group,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 14
    TITLE = "Docking Data"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        parsed = parse_lines(
            puzzle_input,
            (r"mask = ([X10]+)", str_processor_group(1)),
            (r"mem\[(\d+)\] = (\d+)", int_tuple_processor),
        )
        mask = ""
        self.input: List[Tuple[str, int, int]] = []
        for line in parsed:
            if isinstance(line, str):
                mask = line
            elif isinstance(line, tuple):
                memory, value = line
                self.input.append((mask, memory, value))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        memory = {
            location: int(
                "".join([m if m in "01" else v for m, v in zip(mask, f"{value:036b}")]),
                base=2,
            )
            for mask, location, value in self.input
        }

        return sum(memory.values())

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        memory = {}
        for mask, location, value in self.input:
            binary = [v if m == "0" else m for m, v in zip(mask, f"{location:036b}")]
            floating_locations = [i for i, v in enumerate(binary) if v == "X"]
            for x in range(int(pow(2, len(floating_locations)))):
                bits = "{0:0{1:}b}".format(x, len(floating_locations))
                for i, b in zip(floating_locations, bits):
                    binary[i] = b
                memory[int("".join(binary), 2)] = value

        return sum(memory.values())


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
