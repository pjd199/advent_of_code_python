"""Solves the puzzle for Day 6 of Advent of Code 2019.

Universal Orbit Map

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/6
"""
from collections import deque
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 6
    TITLE = "Universal Orbit Map"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input, (r"([A-Z0-9]+)\)([A-Z0-9]+)", str_tuple_processor)
        )
        self.ready = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._prepare_to_solve()

        # perform a breadth first search to find the result
        queue: deque[tuple[str, int]] = deque([("COM", 0)])
        result = 0
        while queue:
            item, orbits = queue.popleft()
            result += orbits
            queue.extend((move, orbits + 1) for move in self.orbited_by.get(item, []))

        return result

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._prepare_to_solve()

        # perform a breadth first search to find the result
        queue: deque[tuple[str, int]] = deque([("YOU", 0)])
        visited = set("YOU")
        result = 0
        while queue:
            item, steps = queue.popleft()

            # have we reached the end?
            if item == "SAN":
                result = steps - 2
                break

            # find the next moves
            moves = []
            if item in self.orbiting:
                moves.append(self.orbiting[item])
            if item in self.orbited_by:
                moves.extend(self.orbited_by[item])

            for move in moves:
                if move not in visited:
                    visited.add(move)
                    queue.append((move, steps + 1))

        return result

    def _prepare_to_solve(self) -> None:
        """Convert the input into dictionaries for ease of lookup."""
        if not self.ready:
            self.orbited_by: dict[str, list[str]] = {a: [] for a, _ in self.input}
            for a, b in self.input:
                self.orbited_by[a].append(b)

            self.orbiting = {b: a for a, b in self.input}
            self.ready = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
