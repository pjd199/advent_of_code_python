"""Solves the puzzle for Day 4 of Advent of Code 2023.

Scratchcards

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/4
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 4
    TITLE = "Scratchcards"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = {
            int(card): (set(winning.split()), set(numbers.split()))
            for card, winning, numbers in parse_lines(
                puzzle_input,
                (r"Card +(\d+): ([0-9 ]+) \| ([0-9 ]+)", str_tuple_processor),
            )
        }

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            2 ** (len(winning & numbers) - 1)
            for winning, numbers in self.input.values()
            if winning & numbers
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        cards = {card: 1 for card in self.input}
        for card, (winning, numbers) in self.input.items():
            for i in range(card + 1, card + 1 + len(winning & numbers)):
                cards[i] += cards[card]
        return sum(cards.values())


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
