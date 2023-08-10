"""Solves the puzzle for Day 24 of Advent of Code 2022.

Blizzard Basin

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/24
"""
from collections import deque
from collections.abc import Generator
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 24
    TITLE = "Blizzard Basin"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"[#^>v<.]", str_processor))
        self.start = (self.input[0].index("."), 0)
        self.finish = (self.input[-1].index("."), len(self.input) - 1)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve([self.start, self.finish])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve([self.start, self.finish, self.start, self.finish])

    def _safe_places(self) -> Generator[frozenset[tuple[int, int]], None, None]:
        """Iterate over the safe places in the map for each minute that passes.

        Yields:
            Generator[frozenset[tuple[int, int]], None, None]: set of co-ordinates
        """
        # calculate the extent of the grid bounded by the valley walls
        min_x, min_y = (1, 1)
        max_x, max_y = (len(self.input[min_y]) - 2, len(self.input) - 2)

        # locate all the points, and each of the blizzards by direction
        all_points = {
            (x, y)
            for y in range(len(self.input))
            for x in range(len(self.input[y]))
            if self.input[y][x] != "#"
        }
        up = {(x, y) for x, y in all_points if self.input[y][x] == "^"}
        right = {(x, y) for x, y in all_points if self.input[y][x] == ">"}
        down = {(x, y) for x, y in all_points if self.input[y][x] == "v"}
        left = {(x, y) for x, y in all_points if self.input[y][x] == "<"}

        # find the safes places using set operations, then move all the blizzards
        while True:
            yield frozenset(all_points - up - right - down - left)
            up = {(x, y - 1 if y > min_y else max_y) for x, y in up}
            right = {(x + 1 if x < max_x else min_x, y) for x, y in right}
            down = {(x, y + 1 if y < max_y else min_y) for x, y in down}
            left = {(x - 1 if x > min_x else max_x, y) for x, y in left}

    def _solve(self, route: list[tuple[int, int]]) -> int:
        """Solve the puzzle.

        Args:
            route (list[tuple[int, int]]): a list of points to visit

        Returns:
            int: the total elapsed time
        """
        safe_iter = self._safe_places()
        states: list[frozenset[tuple[int, int]]] = []

        result = 0
        for (x1, y1), (x2, y2) in zip(route, route[1:]):
            # perform a breadth first search from between the two points
            queue = deque([(x1, y1, result)])
            visited = set(queue)

            while queue:
                x, y, time = queue.popleft()

                # is this the end?
                if (x, y) == (x2, y2):
                    result = time
                    break

                # calculate new states as needed
                while time + 1 >= len(states):
                    states.append(next(safe_iter))

                next_moves = [
                    (move_x, move_y)
                    for move_x, move_y in [
                        (x, y),
                        (x, y - 1),
                        (x + 1, y),
                        (x, y + 1),
                        (x - 1, y),
                    ]
                    if (move_x, move_y) in states[time + 1]
                ]
                for move_x, move_y in next_moves:
                    next_move = (move_x, move_y, time + 1)
                    if next_move not in visited:
                        visited.add(next_move)
                        queue.append(next_move)

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
