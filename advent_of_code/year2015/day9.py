"""Solution for day 9 of Advent of Code 2015."""
from itertools import permutations
from pathlib import Path
from re import compile
from sys import maxsize, path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solver for the puzzle."""

    YEAR = 2015
    DAY = 9
    TITLE = "All in a Single Night"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        pattern = compile(
            r"(?P<a>[A-Za-z]+) to " r"(?P<b>[A-Za-z]+) = " r"(?P<dist>[0-9]+)"
        )
        self.cities = set()
        self.routes = {}
        for i, line in enumerate(puzzle_input):
            match = pattern.fullmatch(line)
            if match:
                a, b, dist = match.group("a", "b", "dist")
                self.cities.add(a)
                self.cities.add(b)
                self.routes[(a, b)] = int(dist)
                self.routes[(b, a)] = int(dist)
            else:
                raise RuntimeError(f"Parse error at line {i+1}: {line}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # loop through every permutation of the cities, finding the shortest
        # possible route
        shortest_distance = maxsize
        for perm in permutations(self.cities):
            total = sum(map(lambda x, y: self.routes[(x, y)], perm[:-1], perm[1:]))
            shortest_distance = min(shortest_distance, total)

        # store the results
        return shortest_distance

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # loop through every permutation of the cities, finding the
        # longest possible route
        longest_distance = 0
        for perm in permutations(self.cities):
            total = sum(map(lambda x, y: self.routes[(x, y)], perm[:-1], perm[1:]))
            longest_distance = max(longest_distance, total)

        return longest_distance


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
