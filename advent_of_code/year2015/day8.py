"""Solution for day 1 of Advent of Code 2015."""
from pathlib import Path
from re import compile
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

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

        self.puzzle_input = []
        pattern = compile(r'".*"')
        for i, line in enumerate(puzzle_input):
            match = pattern.match(line)
            if match:
                self.puzzle_input.append(line)
            else:
                raise RuntimeError(f"Parse error on line {i+1}: {line}")

        self.input = puzzle_input

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
