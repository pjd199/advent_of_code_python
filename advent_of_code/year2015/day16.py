"""Solution for day 16 of Advent of Code 2015."""
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

    UNKNOWN_SUE = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    YEAR = 2015
    DAY = 16
    TITLE = "Aunt Sue"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if puzzle_input is None or len(puzzle_input) == 0:
            raise RuntimeError("Puzzle input is empty")

        self.list_of_sues = []
        pattern = compile(
            r"Sue (?P<num>[0-9]+): "
            r"(?P<a>[a-z]+): (?P<a_val>[0-9]+), "
            r"(?P<b>[a-z]+): (?P<b_val>[0-9]+), "
            r"(?P<c>[a-z]+): (?P<c_val>[0-9]+)"
        )
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                self.list_of_sues.append(
                    dict(
                        {
                            match["a"]: match["a_val"],
                            match["b"]: match["b_val"],
                            match["c"]: match["c_val"],
                        }
                    )
                )
            else:
                raise RuntimeError(f"Parse error on line {i + 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # solve part one
        result = -1
        for i, sue in enumerate(self.list_of_sues):
            if all([int(sue[k]) == Solver.UNKNOWN_SUE[k] for k in sue.keys()]):
                result = i + 1
                break

        return result

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        result = -1
        for i, sue in enumerate(self.list_of_sues):
            matches = []
            for k in sue.keys():
                if k == "cats" or k == "trees":
                    matches.append(int(sue[k]) > Solver.UNKNOWN_SUE[k])
                elif k == "pomeranians" or k == "goldfish":
                    matches.append(int(sue[k]) < Solver.UNKNOWN_SUE[k])
                else:
                    matches.append(int(sue[k]) == Solver.UNKNOWN_SUE[k])
            if all(matches):
                result = i + 1
                break

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
