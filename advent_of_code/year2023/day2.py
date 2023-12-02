"""Solves the puzzle for Day 2 of Advent of Code 2023.

Cube Conundrum

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/2
"""
from dataclasses import dataclass
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    parse_tokens,
    parse_tokens_single_line,
    str_processor,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class RBG:
    """The cubes."""

    red: int = 0
    green: int = 0
    blue: int = 0


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 2
    TITLE = "Cube Conundrum"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = {
            int(game): [
                RBG(**dict(x))
                for x in parse_tokens(
                    parse_tokens_single_line(
                        [data], (r"([a-z0-9, ]*)", str_processor), delimiter=";"
                    ),
                    (r" ?(\d+) (red|green|blue)", lambda m: (m[2], int(m[1]))),
                    delimiter=",",
                    require_delimiter=False,
                )
            ]
            for game, data in parse_lines(
                puzzle_input, (r"Game (\d+): (.*)", str_tuple_processor)
            )
        }

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            game
            for game, data in self.input.items()
            if all(d.red <= 12 and d.green <= 13 and d.blue <= 14 for d in data)
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            (
                max(d.red for d in data)
                * max(d.green for d in data)
                * max(d.blue for d in data)
            )
            for data in self.input.values()
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
