"""Solves the puzzle for Day 13 of Advent of Code 2015.

Knights of the Dinner Table

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/13
"""
from itertools import chain, permutations
from pathlib import Path
from sys import path
from typing import Dict, List, Set, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 13
    TITLE = "Knights of the Dinner Table"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        tuples = parse_lines(
            puzzle_input,
            (
                r"(?P<a>[A-Za-z]+) would "
                r"(?P<sign>gain|lose) "
                r"(?P<value>[0-9]+) happiness units by sitting next to "
                r"(?P<b>[A-Za-z]+).",
                str_tuple_processor,
            ),
        )
        self.names = {a for a, _, _, _ in tuples}
        self.names.update({b for _, _, _, b in tuples})
        self.values = {
            (a, b): int(value) for a, sign, value, b in tuples if sign == "gain"
        }
        self.values.update(
            {(a, b): -int(value) for a, sign, value, b in tuples if sign == "lose"}
        )

    @cache_result
    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._find_optimal(self.names, self.values)

    @cache_result
    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # add "Me" to the table
        names_with_me = self.names | {"Me"}
        values_with_me = dict(self.values)
        values_with_me.update({("Me", x): 0 for x in self.names})
        values_with_me.update({(x, "Me"): 0 for x in self.names})

        # solve the puzzle
        return self._find_optimal(names_with_me, values_with_me)

    def _find_optimal(self, names: Set[str], values: Dict[Tuple[str, str], int]) -> int:
        """Find the optimal searing arrangement for these guests.

        Args:
            names (Set[str]): The names of the guest
            values (Dict[tuple[str, str], int]): the happiness values

        Returns:
            int : the result
        """
        # create a dictionary of the values of each pairing of guests
        # seated next to one another
        pair_values = {
            perm: (values[(perm[0], perm[1])] + values[(perm[1], perm[0])])
            for perm in permutations(names, 2)
        }

        # return the maximum of all the pairings on the round table,
        # so that the pairs i the permuation, plus the wrap around of
        # first pair to last pair
        return max(
            [
                sum(
                    chain(
                        [pair_values[(perm[0], perm[-1])]],
                        [pair_values[(x, y)] for x, y in zip(perm, perm[1:])],
                    )
                )
                for perm in permutations(names)
            ]
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
