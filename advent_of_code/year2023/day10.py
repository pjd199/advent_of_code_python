"""Solves the puzzle for Day 10 of Advent of Code 2023.

Pipe Maze

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/10
"""
from collections import deque
from collections.abc import Iterator
from enum import Enum, auto, unique
from pathlib import Path
from sys import path
from typing import ClassVar

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Directions(Enum):
    """Direction enum."""

    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 10
    TITLE = "Pipe Maze"

    vectors: ClassVar[dict[Directions, tuple[int, int]]] = {
        Directions.NORTH: (0, -1),
        Directions.EAST: (1, 0),
        Directions.SOUTH: (0, 1),
        Directions.WEST: (-1, 0),
    }

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[|\-LJ7F.S]", str_processor)

    def pipe(self) -> Iterator[tuple[int, int]]:
        """Iterator the pipe co-ordinates, starting at S.

        Yields:
            Iterator[tuple[int, int]]: (x, y) for the pipe
        """
        movements = {
            Directions.NORTH: {
                "|": Directions.NORTH,
                "7": Directions.WEST,
                "F": Directions.EAST,
            },
            Directions.EAST: {
                "J": Directions.NORTH,
                "-": Directions.EAST,
                "7": Directions.SOUTH,
            },
            Directions.SOUTH: {
                "J": Directions.WEST,
                "|": Directions.SOUTH,
                "L": Directions.EAST,
            },
            Directions.WEST: {
                "F": Directions.SOUTH,
                "-": Directions.WEST,
                "L": Directions.NORTH,
            },
        }

        def add_elements(*args: tuple[int, int]) -> tuple[int, int]:
            return tuple(sum(values) for values in zip(*args))

        # work out the start location and direction
        x, y = next((x, y) for (x, y), v in self.input.items() if v == "S")
        direction = next(
            d
            for d in Directions
            if self.input.get(add_elements((x, y), self.vectors[d]), ".")
            in movements[d]
        )

        # follow the path
        steps = 0
        while True:
            yield (x, y)
            x, y = add_elements((x, y), self.vectors[direction])
            steps += 1
            if self.input[(x, y)] == "S":
                break
            direction = movements[direction][self.input[(x, y)]]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(1 for _ in self.pipe()) // 2

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # enlarge the grid to open up the gaps
        scale = 3

        # add the corners to the grid
        grid = {
            (x * scale, y * scale): self.input[(x, y)]
            for (x, y) in self.pipe()
            if self.input[(x, y)] in "LJ7FS"
        }
        (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*grid))

        # connect the corners with the pipes
        corners = {
            "LJ": Directions.NORTH,
            "FL": Directions.EAST,
            "F7": Directions.SOUTH,
            "J7": Directions.WEST,
        }
        for (x, y), v in list(grid.items()):
            for corner, direction in corners.items():
                if v in corner:
                    vector = self.vectors[direction]
                    x1, y1 = tuple(sum(values) for values in zip((x, y), vector))
                    while (x1, y1) not in grid:
                        grid[(x1, y1)] = (
                            "-"
                            if direction in (Directions.EAST, Directions.WEST)
                            else "|"
                        )
                        x1, y1 = tuple(sum(values) for values in zip((x1, y1), vector))

        # flood fill the outside, starting at (min_x, min_y)
        queue = deque([(min_x, min_y)])
        while queue:
            x, y = queue.popleft()
            if (x, y) not in grid:
                grid[(x, y)] = "O"
                queue.extend(
                    (x1, y1)
                    for x1, y1 in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
                    if min_x - (2 * scale) <= x <= max_x + (2 * scale)
                    and min_y - (2 * scale) <= y <= max_y + (2 * scale)
                    and (x1, y1) not in grid
                )

        # count the squares that are not pipes or marked as outside
        return sum(
            1
            for y in range(0, max_y + 1, scale)
            for x in range(0, max_x + 1, scale)
            if (x, y) not in grid
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
