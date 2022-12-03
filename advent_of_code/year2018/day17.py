"""Solves the puzzle for Day 17 of Advent of Code 2018.

Reservoir Research

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/17
"""
from collections import defaultdict, deque
from copy import deepcopy
from pathlib import Path
from sys import path
from typing import Deque, Dict, List, Set, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 17
    TITLE = "Reservoir Research"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        parsed = parse_lines(
            puzzle_input,
            (
                r"([xy])=(\d+), [xy]=(\d+)..(\d+)",
                lambda m: (m[1], int(m[2]), int(m[3]), int(m[4])),
            ),
        )
        self.input: Dict[Tuple[int, int], str] = defaultdict(lambda: ".")

        for x_or_y, a, b, c in parsed:
            if x_or_y == "x":
                min_x, max_x = a, a
                min_y, max_y = b, c
            else:
                min_x, max_x = b, c
                min_y, max_y = a, a
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    self.input[(x, y)] = "#"

        self.flowing: Set[Tuple[int, int]] = set()
        self.standing: Set[Tuple[int, int]] = set()

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.flowing or not self.standing:
            self._solve()

        return len(self.flowing) + len(self.standing)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.flowing or not self.standing:
            self._solve()

        return len(self.standing)

    def _solve(self) -> None:
        """Solve the puzzle."""
        spring = (500, 0)
        grid = deepcopy(self.input)
        grid[spring] = "+"

        min_y = min(y for x, y in grid.keys() if grid[(x, y)] == "#")
        max_y = max(y for x, y in grid.keys() if grid[(x, y)] == "#")

        # expand the flow of water, breadth first search style
        flows: Deque[Tuple[int, int]] = deque()
        flows.append(spring)
        while flows:
            x, y = flows.popleft()

            if y < max_y:
                if grid[(x, y + 1)] == ".":
                    # flow down
                    grid[(x, y + 1)] = "v"
                    flows.append((x, y + 1))
                if grid[(x, y + 1)] in "~#" and grid[(x - 1, y)] == ".":
                    # flow left
                    grid[(x - 1, y)] = "v"
                    flows.append((x - 1, y))
                if grid[(x, y + 1)] in "~#" and grid[(x + 1, y)] == ".":
                    # flow right
                    grid[(x + 1, y)] = "v"
                    flows.append((x + 1, y))

            # check if a pool has formed
            if (
                grid[(x - 1, y)] in "v#"
                and grid[(x - 1, y)] != "."
                and grid[(x + 1, y)] in "v#"
                and grid[(x + 1, y)] != "."
            ):
                # check for extend of water
                left, right = x, x
                while grid[(left - 1, y)] == "v":
                    left -= 1
                while grid[(right + 1, y)] == "v":
                    right += 1

                # check for pool boundaries
                if (
                    grid[(left - 1, y)] == "#"
                    and grid[(right + 1, y)] == "#"
                    and all(
                        grid[(x1, y + 1)] in "#~" for x1 in range(left - 1, right + 2)
                    )
                ):
                    # found a pool, so update the grid and include the feed streams
                    # in the flow queue
                    grid.update({(x1, y): "~" for x1 in range(left, right + 1)})
                    flows.extend(
                        [
                            (x1, y - 1)
                            for x1 in range(left, right + 1)
                            if grid[(x1, y - 1)] == "v"
                        ]
                    )

        self.flowing = {
            k for k, v in grid.items() if v == "v" and min_y <= k[1] <= max_y
        }
        self.standing = {
            k for k, v in grid.items() if v == "~" and min_y <= k[1] <= max_y
        }


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
