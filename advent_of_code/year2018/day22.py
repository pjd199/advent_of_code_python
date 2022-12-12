"""Solves the puzzle for Day 22 of Advent of Code 2018.

Mode Maze

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/22
"""
from collections import deque
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Deque, List, Set, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Terrain(Enum):
    """Type of cave."""

    ROCKY = 0
    WET = 1
    NARROW = 2


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 22
    TITLE = "Mode Maze"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        parsed = parse_lines(
            puzzle_input,
            (r"depth: (\d+)", int_tuple_processor),
            (r"target: (\d+),(\d+)", int_tuple_processor),
        )
        self.depth = parsed[0][0]
        self.target_x, self.target_y = parsed[1]

        self.terrain: List[List[Terrain]] = []
        self.risk: List[List[int]] = []

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.risk:
            self._create_map()

        return sum(
            sum(row[: self.target_x + 1]) for row in self.risk[: self.target_y + 1]
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.terrain:
            self._create_map()

        @unique
        class Gear(Enum):
            NEITHER = 0
            CLIMBING = 1
            TORCH = 2

        allowed = {
            Terrain.ROCKY: {
                Gear.NEITHER: False,
                Gear.CLIMBING: True,
                Gear.TORCH: True,
            },
            Terrain.WET: {
                Gear.NEITHER: True,
                Gear.CLIMBING: True,
                Gear.TORCH: False,
            },
            Terrain.NARROW: {
                Gear.NEITHER: True,
                Gear.CLIMBING: False,
                Gear.TORCH: True,
            },
        }

        queue: Deque[Tuple[int, int, Gear, int, int]] = deque(
            [(0, 0, Gear.TORCH, 0, 0)]
        )  # (x, y, tool, time, wait)
        visited: Set[Tuple[int, int, Gear]] = set()

        result = -1
        while queue:
            x, y, tool, time, wait = queue.popleft()

            # check if we are still waiting to change tools
            if wait > 0:
                queue.append((x, y, tool, time + 1, wait - 1))
                continue

            # mark this point as visited
            visited.add((x, y, tool))

            # check if we have reached the target and holding the TORCH
            if (x, y, tool) == (self.target_x, self.target_y, Gear.TORCH):
                result = time
                break

            # explore all the valid moves with this tool
            moves = [
                (x1, y1)
                for x1, y1 in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
                if 0 <= y1 < len(self.terrain) and 0 <= x1 < len(self.terrain[y1])
            ]
            for x1, y1 in moves:
                if (
                    allowed[self.terrain[y1][x1]][tool]
                    and (x1, y1, tool) not in visited
                ):
                    visited.add((x1, y1, tool))
                    queue.append((x1, y1, tool, time + 1, 0))

            # change the tool, if allowed
            for t1 in Gear:
                if allowed[self.terrain[y][x]][t1] and (x, y, t1) not in visited:
                    queue.appendleft((x, y, t1, time, 7))

        return result

    def _create_map(self) -> None:
        """Create the terrain map."""
        width = self.target_x + 100
        height = self.target_y + 100

        geologic = [[0] * width for _ in range(height)]
        erosion = [[0] * width for _ in range(height)]
        self.terrain = [[Terrain.ROCKY] * width for _ in range(height)]
        self.risk = [[0] * width for _ in range(height)]

        for y in range(height):
            for x in range(width):
                if (x, y) in [(0, 0), (self.target_x, self.target_y)]:
                    geologic[y][x] = 0
                elif y == 0:
                    geologic[y][x] = 16807 * x
                elif x == 0:
                    geologic[y][x] = 48271 * y
                else:
                    geologic[y][x] = erosion[y][x - 1] * erosion[y - 1][x]
                erosion[y][x] = (geologic[y][x] + self.depth) % 20183
                self.terrain[y][x] = Terrain(erosion[y][x] % 3)
                self.risk[y][x] = self.terrain[y][x].value


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
