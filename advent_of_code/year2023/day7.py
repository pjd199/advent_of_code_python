"""Solves the puzzle for Day 7 of Advent of Code 2023.

Camel Cards

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/7
"""
from collections import Counter
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 7
    TITLE = "Camel Cards"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"([AKQJT98765432]{5}) (\d+)", lambda m: (m[1], int(m[2])))
        )

    def type_order(self, cards: str) -> int:
        """Find the type order, highest is strongest.

        Args:
            cards (str): the cards in hand

        Returns:
            int: the strength
        """
        match sorted(Counter(cards).values()):
            case (5,):  # Five of a kind
                result = 7
            case (1, 4):  # Foud of a kind
                result = 6
            case (2, 3):  # Full house
                result = 5
            case (1, 1, 3):  # Three of a kind
                result = 4
            case (1, 2, 2):  # Two pair
                result = 3
            case (1, 1, 1, 2):  # One pair
                result = 2
            case (1, 1, 1, 1, 1):  # High card
                result = 1
        return result

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """

        def key(hand: tuple[str, int]) -> tuple[int, ...]:
            cards, _ = hand
            values = "23456789TJQKA"
            return (self.type_order(cards), *(values.index(x) for x in cards))

        return sum(
            (rank + 1) * bid
            for rank, (_, bid) in enumerate(sorted(self.input, key=key))
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        def key(hand: tuple[str, int]) -> tuple[int, ...]:
            cards, _ = hand
            values = "J23456789TQKA"
            return (
                max(
                    self.type_order(cards.replace("J", joker))
                    for joker in "23456789TQKA"
                ),
                *(values.index(x) for x in cards),
            )

        return sum(
            (rank + 1) * bid
            for rank, (_, bid) in enumerate(sorted(self.input, key=key))
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
