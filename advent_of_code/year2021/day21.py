"""Solves the puzzle for Day 21 of Advent of Code 2021.

Dirac Dice

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/21
"""
from collections.abc import Generator
from functools import cache
from itertools import cycle, product
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor_group, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 21
    TITLE = "Dirac Dice"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (r"Player \d+ starting position: (\d+)", int_processor_group(1)),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """

        def dice_iter() -> Generator[int, None, None]:
            dice = 1
            while True:
                yield dice
                dice = 1 if dice == 100 else dice + 1

        scores = [0, 0]
        positions = [x - 1 for x in self.input.copy()]

        throw = dice_iter()
        player_iter = cycle([0, 1])
        count = 0
        while max(scores) < 1000:
            player = next(player_iter)
            positions[player] = (
                positions[player] + next(throw) + next(throw) + next(throw)
            ) % 10
            scores[player] += positions[player] + 1
            count += 3

        return min(scores) * count

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        @cache
        def play(
            position1: int, score1: int, position2: int, score2: int
        ) -> tuple[int, int]:
            win1 = win2 = 0
            for dice in product([1, 2, 3], [1, 2, 3], [1, 2, 3]):
                new_position1 = (position1 + sum(dice)) % 10
                new_score1 = score1 + new_position1 + 1
                if new_score1 >= 21:
                    win1 += 1
                else:
                    win2_delta, win1_delta = play(
                        position2, score2, new_position1, new_score1
                    )
                    win1 += win1_delta
                    win2 += win2_delta
            return win1, win2

        positions = [x - 1 for x in self.input.copy()]
        return max(play(positions[0], 0, positions[1], 0))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
