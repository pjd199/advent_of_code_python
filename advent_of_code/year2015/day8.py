"""Solves the puzzle for Day 8 of Advent of Code 2015.

Matchsticks

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/8
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 8
    TITLE = "Matchsticks"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r'"[a-z0-9"\\]+"', str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        literal_length = 0
        memory_length = 0
        for line in self.input:
            line = line.strip()
            literal_length += len(line)
            result = []
            i = 1
            while i < (len(line) - 1):
                if line[i : i + 2] == r"\x":
                    result.append(chr(int(line[i + 2 : i + 4], 16)))
                    i += 4
                elif line[i : i + 2] == r"\\":
                    result.append("\\")
                    i += 2
                elif line[i : i + 2] == r"\"":
                    result.append('"')
                    i += 2
                else:
                    result.append(line[i])
                    i += 1
            memory_length += len("".join(result))
        return literal_length - memory_length

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        literal_length = 0
        encoded_length = 0
        for line in self.input:
            line = line.strip()
            literal_length += len(line)
            result = ['"']
            for character in line:
                if character == '"':
                    result.append('\\"')
                elif character == "\\":
                    result.append("\\\\")
                else:
                    result.append(character)
            result.append('"')
            encoded_length += len("".join(result))

        return encoded_length - literal_length


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
