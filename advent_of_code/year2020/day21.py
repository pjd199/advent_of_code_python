"""Solves the puzzle for Day 21 of Advent of Code 2020.

Allergen Assessment

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/21
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    parse_tokens_single_line,
    str_processor,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 21
    TITLE = "Allergen Assessment"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        parsed = parse_lines(
            puzzle_input, (r"([a-z ]+)\(contains ([a-z, ]+)\)", str_tuple_processor)
        )
        self.ingredients = [
            set(
                parse_tokens_single_line(
                    [line],
                    (r"[a-z]+", str_processor),
                    delimiter=" ",
                    require_delimiter=False,
                )
            )
            for line, _ in parsed
        ]
        self.allergens = [
            set(
                parse_tokens_single_line(
                    [line],
                    (r"[a-z]+", str_processor),
                    delimiter=", ",
                    require_delimiter=False,
                )
            )
            for _, line in parsed
        ]
        self.ready = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._prepare()
        return sum(
            1
            for row in self.ingredients
            for ingredient in row
            if ingredient in self.safe_to_eat
        )

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        self._prepare()
        ingredients = [i - self.safe_to_eat for i in self.ingredients]
        options = {
            a: set.intersection(
                *[
                    ingredients[i]
                    for i in range(len(ingredients))
                    if a in self.allergens[i]
                ]
            )
            for a in self.all_allergens
        }

        results: dict[str, str] = {}
        while options:
            for k in list(options.keys()):
                if len(options[k]) == 1:
                    found = options[k].pop()
                    results[k] = found
                    for value in options.values():
                        value.discard(found)
                    del options[k]

        return ",".join([results[a] for a in sorted(results.keys())])

    def _prepare(self) -> None:
        """Prepare the safe to eat list."""
        if self.ready:
            return

        self.all_allergens = set().union(*self.allergens)
        self.all_ingredients = set().union(*self.ingredients)

        self.safe_to_eat = self.all_ingredients - set().union(
            *[
                set.intersection(
                    *[
                        i
                        for i, a in zip(self.ingredients, self.allergens)
                        if allergen in a
                    ]
                )
                for allergen in self.all_allergens
            ]
        )
        self.ready = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
