"""Solves the puzzle for Day 19 of Advent of Code 2015.

Medicine for Rudolph

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/19
"""
from pathlib import Path
from sys import path
from typing import List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    parse_single_line,
    split_sections,
    str_processor,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 19
    TITLE = "Medicine for Rudolph"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input, expected_sections=2)

        self.replacements = [
            (a, b)
            for a, b in parse_lines(
                sections[0],
                (r"(?P<a>[a-zA-Z]+) => (?P<b>[a-zA-Z]+)", str_tuple_processor),
            )
        ]
        self.medication = parse_single_line(sections[1], r"[A-Za-z]+", str_processor)

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return len(self._replace(self.medication, self.replacements))

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve part two by working back from the medicine to "e",
        # repeatedly finding the shortest next option of all the
        # possible replacements using min to find the shortest
        # string in a list
        steps = 0
        options = self._replace(self.medication, self.replacements, reverse=True)
        while options:
            options = self._replace(
                min(options, key=len), self.replacements, reverse=True
            )
            steps += 1
        return steps

    def _replace(
        self,
        molecule: str,
        replacement_list: List[Tuple[str, str]],
        reverse: bool = False,
    ) -> List[str]:
        """Create a list of all the possible new molecules.

        Args:
            molecule (str): the input molecule
            replacement_list (List[Tuple[str, ...]]): list of replacements
            reverse (bool): if True, reverses the replacement_list.
                Defaults to False.

        Returns:
            List[str]: a list of all the possible replacements
        """
        results = set()
        for a, b in replacement_list:
            if reverse:
                a, b = b, a

            results.update(
                [
                    molecule[:i] + b + molecule[i + len(a) :]
                    for i in range(len(molecule))
                    if molecule[i : i + len(a)] == a
                ]
            )
        return list(results)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
