"""Solution for day 13 of Advent of Code 2015."""
from itertools import chain, permutations
from re import compile
from typing import Dict, List, Set, Tuple

from advent_of_code.utils.solver_interface import SolverInterface


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

        # parse the input into a set of names and
        # a dictionary of name pairs to values
        pattern = compile(
            r"(?P<a>[A-Za-z]+) would "
            r"(?P<sign>(gain|lose)) "
            r"(?P<value>[0-9]+) happiness units by sitting next to "
            r"(?P<b>[A-Za-z]+)."
        )
        self.names = set()
        self.values = {}
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                a, b, sign, value = match.group("a", "b", "sign", "value")
                self.names.add(a)
                self.names.add(b)
                if sign == "gain":
                    self.values[(a, b)] = int(value)
                else:
                    self.values[(a, b)] = -int(value)
            else:
                raise RuntimeError(f"Parse error on line {i + 1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._find_optimal(self.names, self.values)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # solve the puzzle
        return self._find_optimal(
            self.names | {"Me"},
            (
                self.values
                | {("Me", x): 0 for x in self.names}
                | {(x, "Me"): 0 for x in self.names}
            ),
        )

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
