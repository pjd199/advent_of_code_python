"""Solves the puzzle for Day 20 of Advent of Code 2020.

Jurassic Jigsaw

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/20
"""
from collections import deque
from collections.abc import Callable
from math import prod
from pathlib import Path
from re import finditer
from sys import path
from typing import TypeVar

import numpy as np
from numpy.typing import NDArray

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    int_processor_group,
    parse_single_line,
    parse_tokens,
    split_sections,
    str_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface

T = TypeVar("T", np.str_, np.bool_)


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 20
    TITLE = "Jurassic Jigsaw"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = {
            parse_single_line(
                section[0:1], r"Tile (\d+):", int_processor_group(1)
            ): parse_tokens(
                section,
                (r"[.#]", str_processor),
                header=(r"Tile \d+:",),
                min_length=2,
            )
            for section in split_sections(puzzle_input)
        }
        self.ready = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._arrange_grid()
        return prod(
            [
                self.locations[0][0],  # top left
                self.locations[0][-1],  # top right
                self.locations[-1][0],  # bottom left
                self.locations[-1][-1],  # bottom right
            ]
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._arrange_grid()

        # the icon of a sea monster to find in the photo
        icon = [
            r"..................#.",
            r"#....##....##....###",
            r".#..#..#..#..#..#...",
        ]
        icon_array = np.array([[x == "#" for x in row] for row in icon])

        # arrange the grid, then create views of therotations and flips
        photo_arrays = self._rotations_and_flips(self.photo)
        results_array = np.full_like(self.photo, False, dtype=np.bool_)
        results_arrays = self._rotations_and_flips(results_array)

        # search for the sea monster icon in the photo using regular expressions,
        # storing the locations in the results array
        for photo, result in zip(photo_arrays, results_arrays):
            photo_str = ["".join(row) for row in photo]
            for y in range(len(photo_str) - 2):
                matches = [
                    {
                        m.start()
                        for m in finditer(rf"(?=(?:{icon[i]}))", photo_str[y + i])
                    }
                    for i in range(len(icon))
                ]
                if all(m for m in matches):
                    full_match = matches[0] & matches[1] & matches[2]
                    for x in full_match:
                        result[
                            y : y + len(icon_array), x : x + len(icon_array[0])
                        ] |= icon_array

        return len(self.photo[(results_array == 0) & (self.photo == "#")])

    def _arrange_grid(self) -> None:
        """Arrange the tiles into a grid."""
        if self.ready:
            return

        # create all the rotations and flip views of each tile array
        tiles = {
            identifier: self._rotations_and_flips(np.array(values))
            for identifier, values in self.input.items()
        }

        # perform a breadth first search to arrange the tiles into the grid
        start = next(k for k in self.input)
        queue: deque[tuple[int, int]] = deque([(0, 0)])

        grid: dict[tuple[int, int], NDArray[np.str_]] = {(0, 0): tiles[start][0]}
        visited: dict[tuple[int, int], int] = {(0, 0): start}
        tiles_not_yet_placed = {t for t in self.input if t != start}

        while queue:
            x, y = queue.popleft()

            moves: list[
                tuple[
                    tuple[int, int],
                    Callable[[NDArray[np.str_], NDArray[np.str_]], bool],
                ]
            ] = [
                (move, function)
                for move, function in [
                    ((x, y - 1), lambda a, b: np.array_equal(a[0], b[-1])),
                    ((x + 1, y), lambda a, b: np.array_equal(a[:, -1], b[:, 0])),
                    ((x, y + 1), lambda a, b: np.array_equal(a[-1], b[0])),
                    ((x - 1, y), lambda a, b: np.array_equal(a[:, 0], b[:, -1])),
                ]
                if move not in visited
            ]

            for move, neighbour_id, rotation in [
                (move, tile, rotation)
                for move, equals in moves
                for tile in tiles_not_yet_placed
                for rotation in tiles[tile]
                if equals(grid[(x, y)], rotation)
            ]:
                grid[move] = rotation
                visited[move] = neighbour_id
                tiles_not_yet_placed.remove(neighbour_id)
                queue.append(move)

        # store the locations and the photo
        (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*grid.keys()))
        self.locations = [
            [visited[(x, y)] for x in range(min_x, max_x + 1)]
            for y in range(min_y, max_y + 1)
        ]
        self.photo = np.array(
            [
                [
                    grid[(grid_x, grid_y)][tile_y][x1]
                    for grid_x in range(min_x, max_x + 1)
                    for x1 in range(1, 9)
                ]
                for grid_y in range(min_y, max_y + 1)
                for tile_y in range(1, 9)
            ]
        )
        self.ready = True

    def _rotations_and_flips(self, array: NDArray[T]) -> list[NDArray[T]]:
        """Create a list of rotated and flipped views of array.

        Args:
            array (NDArray[T]): the input array

        Returns:
            list[NDArray[T]]: the output
        """
        return [
            array,
            np.rot90(array, k=1),
            np.rot90(array, k=2),
            np.rot90(array, k=3),
            np.fliplr(array),
            np.rot90(np.fliplr(array), k=1),
            np.rot90(np.fliplr(array), k=2),
            np.rot90(np.fliplr(array), k=3),
        ]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
