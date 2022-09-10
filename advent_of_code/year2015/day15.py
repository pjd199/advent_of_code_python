"""Solves the puzzle for Day 15 of Advent of Code 2015.

Science for Hungry People

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/15
"""
from itertools import combinations_with_replacement, groupby
from math import prod
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface

PROPERTIES = ["capacity", "durability", "flavor", "texture", "calories"]


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 15
    TITLE = "Science for Hungry People"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.ingredients = dict(
            parse_lines(
                puzzle_input,
                (
                    r"(?P<name>[A-Za-z]+): "
                    r"capacity (?P<capacity>-?[0-9]+), "
                    r"durability (?P<durability>-?[0-9]+), "
                    r"flavor (?P<flavor>-?[0-9]+), "
                    r"texture (?P<texture>-?[0-9]+), "
                    r"calories (?P<calories>-?[0-9]+)",
                    lambda m: (m[0], tuple(int(x) for x in m.groups()[1:])),
                ),
            )
        )
        self.has_run = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.has_run:
            self._bake()

        return self.top_score

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.has_run:
            self._bake()

        return self.top_calorie_counting_score

    def _bake(self) -> None:
        """Run the simulation."""
        self.top_score = 0
        self.top_calorie_counting_score = 0
        for combo in combinations_with_replacement(self.ingredients.keys(), 100):
            property_scores = [0] * len(PROPERTIES)
            recipe = {k: len(list(g)) for k, g in groupby(combo)}
            for item in recipe:
                for x in range(len(property_scores)):
                    property_scores[x] += recipe[item] * self.ingredients[item][x]
            property_scores = [max(x, 0) for x in property_scores]
            score = prod(property_scores[:-1])
            self.top_score = max(score, self.top_score)
            if property_scores[-1] == 500:
                self.top_calorie_counting_score = max(
                    score, self.top_calorie_counting_score
                )

        self.has_run = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
