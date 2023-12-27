"""Solves the puzzle for Day 15 of Advent of Code 2023.

Lens Library

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/15
"""
from functools import reduce
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_tokens_single_line,
    str_processor,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 15
    TITLE = "Lens Library"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input_text = parse_tokens_single_line(
            puzzle_input,
            (r"([a-z]+)([-=])([0-9])?", str_processor),
            delimiter=",",
        )
        self.input_parsed = parse_tokens_single_line(
            puzzle_input,
            (r"([a-z]+)([-=])([0-9])?", str_tuple_processor),
            delimiter=",",
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(self.hash_algorithm(text) for text in self.input_text)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        boxes: list[dict[str, int]] = [{} for _ in range(256)]
        for label, operator, focal in self.input_parsed:
            box = boxes[self.hash_algorithm(label)]
            if operator == "-":
                if label in box:
                    del box[label]
            else:
                box[label] = int(focal)

        return sum(
            (number + 1) * (slot + 1) * focal
            for number, box in enumerate(boxes)
            for slot, focal in enumerate(box.values())
        )

    def hash_algorithm(self, text: str) -> int:
        """HASH the text.

        Args:
            text (str): the input text

        Returns:
            int: the result
        """
        return reduce(lambda value, x: ((value + ord(x)) * 17) % 256, text, 0)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
