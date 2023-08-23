"""Solves the puzzle for Day 12 of Advent of Code 2022.

Hill Climbing Algorithm

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/12
"""
from collections import deque
from copy import deepcopy
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
    DAY = 12
    TITLE = "Hill Climbing Algorithm"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"[a-zSE]", str_processor))

        self.clean_grid = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve()

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # find all the possible starting places
        starts = {
            (x, y)
            for y, row in enumerate(self.input)
            for x, value in enumerate(row)
            if value == "a"
        }
        # find the shortest path, excluding dead end paths
        return min(filter((lambda x: x >= 0), (self._solve(x, y) for x, y in starts)))

    def _solve(self, start_x: int = -1, start_y: int = -1) -> int:
        """Solve the puzzle, finding the shortest path from start to end.

        Args:
            start_x (int): Override the starting x. Defaults to -1.
            start_y (int): Override the starting y. Defaults to -1.

        Returns:
            int: the fewest number of steps from start to end
        """
        if not self.clean_grid:
            self.grid = deepcopy(self.input)

            # find the start and end points in the grid
            route = {
                value: (x, y)
                for y, row in enumerate(self.input)
                for x, value in enumerate(row)
                if value in "SE"
            }
            # save the start location and replace in grid
            self.start = route["S"]
            x, y = self.start
            self.grid[y][x] = "a"

            # save the end location and replace in grid
            self.end = route["E"]
            x, y = self.end
            self.grid[y][x] = "z"

            self.clean_grid = True

        # move the starting position, if required
        if 0 <= start_y < len(self.grid) and 0 <= start_x < len(self.grid[start_y]):
            start = (start_x, start_y)
        else:
            start = self.start

        # perform a breadth first search to find the shortest path from start to end
        queue: deque[tuple[int, int, int]] = deque([(*start, 0)])
        visited = {start}
        result = -1

        while queue:
            x, y, steps = queue.popleft()

            if (x, y) == self.end:
                # reached the end
                result = steps
                break

            # for each potential move
            for x1, y1 in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
                if (
                    0 <= y1 < len(self.grid)
                    and 0 <= x1 < len(self.grid[y1])
                    and ord(self.grid[y1][x1]) <= (ord(self.grid[y][x]) + 1)
                    and (x1, y1) not in visited
                ):
                    # found a valid move
                    queue.append((x1, y1, steps + 1))
                    visited.add((x1, y1))

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
