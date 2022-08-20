"""Solves the puzzle for Day 24 of Advent of Code 2016.

Air Duct Spelunking

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/24
"""
from collections import deque
from itertools import permutations
from pathlib import Path
from sys import maxsize, path
from typing import Callable, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 24
    TITLE = "Air Duct Spelunking"

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

        # parse the input
        self.grid = {}
        self.destinations = {}
        for y, line in enumerate(puzzle_input):
            for x, char in enumerate(line):
                if char in ".#" or char.isnumeric():
                    self.grid[(x, y)] = char
                    if char.isnumeric():
                        self.destinations[char] = (x, y)
                else:
                    raise RuntimeError(f"Unable to parse {line} on line {y+1}")

        self.run_once = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return self.min_to_end

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return self.min_to_home

    def _run(self) -> None:
        """Run the simulation."""
        # only need to run this once
        if self.run_once:
            return
        self.run_once = True

        # functions for the moves
        moves: List[Callable[[int, int], Tuple[int, int]]] = [
            lambda x, y: (x, y - 1),
            lambda x, y: (x + 1, y),
            lambda x, y: (x, y + 1),
            lambda x, y: (x - 1, y),
        ]

        # find distance between each node, using a breadth first search
        distances = {}
        for start in self.destinations:
            queue = deque([(self.destinations[start], int(0))])
            visited = {self.destinations[start]}

            while queue:
                location, steps = queue.popleft()

                # have we found a new destination
                char = self.grid[location]
                if char in self.destinations and char not in distances:
                    distances[(start, char)] = steps
                    distances[(char, start)] = steps
                    if all(
                        (
                            (start, destination) in distances
                            for destination in self.destinations
                        )
                    ):
                        break

                # add all valid next moves to the queue
                for move in moves:
                    new_location = move(*location)
                    if new_location not in visited and (
                        self.grid[new_location] == "."
                        or self.grid[new_location] in self.destinations
                    ):
                        visited.add(new_location)
                        queue.append((new_location, steps + 1))

        # find the shortest routes
        self.min_to_end = maxsize
        self.min_to_home = maxsize
        for route in permutations(self.destinations):
            if route[0] == "0":
                path = sum(distances[(a, b)] for a, b in zip(route, route[1:]))
                self.min_to_end = min(self.min_to_end, path)
                self.min_to_home = min(
                    self.min_to_home, path + distances[(route[-1], "0")]
                )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
