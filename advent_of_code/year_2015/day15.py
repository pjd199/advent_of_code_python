"""Solution for day 15 of Advent of Code 2015."""
from itertools import combinations_with_replacement, groupby
from math import prod
from re import compile
from typing import List, Tuple

from advent_of_code.utils.solver_interface import SolverInterface

PROPERTIES = ["capacity", "durability", "flavor", "texture", "calories"]


class Solver(SolverInterface):
    """Solver for the puzzle."""

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

        pattern = compile(
            r"(?P<name>[A-Za-z]+): "
            r"capacity (?P<capacity>-?[0-9]+), "
            r"durability (?P<durability>-?[0-9]+), "
            r"flavor (?P<flavor>-?[0-9]+), "
            r"texture (?P<texture>-?[0-9]+), "
            r"calories (?P<calories>-?[0-9]+)"
        )
        self.ingredients = {}
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                self.ingredients[match["name"]] = [int(match[p]) for p in PROPERTIES]
            else:
                raise RuntimeError(f"Parse error on line {i + 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        top_score, _ = self._bake()
        return top_score

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        _, top_calorie_counting_score = self._bake()
        return top_calorie_counting_score

    def solve_all(self) -> List[int]:
        """Solve both parts of the puzzle.

        Returns:
            List[int]: the answer
        """
        top_score, top_calorie_counting_score = self._bake()
        return [top_score, top_calorie_counting_score]

    def _bake(self) -> Tuple[int, int]:
        """Run the simulation.

        Returns:
            Tuple[int, int]: the return values for part one and part two
        """
        top_score = 0
        top_calorie_counting_score = 0
        for combo in combinations_with_replacement(self.ingredients.keys(), 100):
            property_scores = [0] * len(PROPERTIES)
            recipe = {k: len(list(g)) for k, g in groupby(combo)}
            for item in recipe:
                for x in range(len(property_scores)):
                    property_scores[x] += recipe[item] * self.ingredients[item][x]
            property_scores = [max(x, 0) for x in property_scores]
            score = prod(property_scores[:-1])
            top_score = max(score, top_score)
            if property_scores[-1] == 500:
                top_calorie_counting_score = max(score, top_calorie_counting_score)

        return top_score, top_calorie_counting_score
