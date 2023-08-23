"""Solves the puzzle for Day 2 of Advent of Code 2022.

Rock Paper Scissors

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/2
"""
from enum import Enum, unique
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Shape(Enum):
    """A shape in the game."""

    Rock = "Rock"
    Paper = "Paper"
    Scissors = "Scissors"


class Outcome(Enum):
    """An outcome in the game."""

    Win = "Win"
    Lose = "Lose"
    Draw = "Draw"


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 2
    TITLE = "Rock Paper Scissors"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"([ABC]) ([XYZ])", str_tuple_processor)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        shapes = {
            "A": Shape.Rock,
            "B": Shape.Paper,
            "C": Shape.Scissors,
            "X": Shape.Rock,
            "Y": Shape.Paper,
            "Z": Shape.Scissors,
        }

        return self._play([(shapes[a], shapes[b]) for a, b in self.input])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        shapes: dict[str, Shape] = {
            "A": Shape.Rock,
            "B": Shape.Paper,
            "C": Shape.Scissors,
        }

        outcomes: dict[str, Outcome] = {
            "X": Outcome.Lose,
            "Y": Outcome.Draw,
            "Z": Outcome.Win,
        }

        decode: dict[tuple[Shape, Outcome], Shape] = {
            (Shape.Rock, Outcome.Lose): Shape.Scissors,
            (Shape.Rock, Outcome.Draw): Shape.Rock,
            (Shape.Rock, Outcome.Win): Shape.Paper,
            (Shape.Paper, Outcome.Lose): Shape.Rock,
            (Shape.Paper, Outcome.Draw): Shape.Paper,
            (Shape.Paper, Outcome.Win): Shape.Scissors,
            (Shape.Scissors, Outcome.Lose): Shape.Paper,
            (Shape.Scissors, Outcome.Draw): Shape.Scissors,
            (Shape.Scissors, Outcome.Win): Shape.Rock,
        }

        return self._play(
            [(shapes[a], decode[shapes[a], outcomes[b]]) for a, b in self.input]
        )

    def _play(self, rounds: list[tuple[Shape, Shape]]) -> int:
        """Play a game of Rock, Paper, Scissors.

        Args:
            rounds (list[tuple[Shape, Shape]]): the input

        Returns:
            int: the results
        """
        shape_score: dict[Shape, int] = {
            Shape.Rock: 1,
            Shape.Paper: 2,
            Shape.Scissors: 3,
        }
        round_score: dict[tuple[Shape, Shape], int] = {
            (Shape.Rock, Shape.Rock): 3,
            (Shape.Rock, Shape.Paper): 6,
            (Shape.Rock, Shape.Scissors): 0,
            (Shape.Paper, Shape.Rock): 0,
            (Shape.Paper, Shape.Paper): 3,
            (Shape.Paper, Shape.Scissors): 6,
            (Shape.Scissors, Shape.Rock): 6,
            (Shape.Scissors, Shape.Paper): 0,
            (Shape.Scissors, Shape.Scissors): 3,
        }
        return sum(
            shape_score[human] + round_score[(elf, human)] for elf, human in rounds
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
