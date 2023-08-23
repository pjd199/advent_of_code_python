"""Solves the puzzle for Day 22 of Advent of Code 2022.

Monkey Map

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/22
"""
from collections import deque
from math import sqrt
from pathlib import Path
from re import split
from sys import maxsize, path

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_grid,
    parse_single_line,
    split_sections,
    str_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 22
    TITLE = "Monkey Map"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        map_section, directions_section = split_sections(
            puzzle_input, expected_sections=2
        )

        self.map = {
            k: v
            for k, v in parse_grid(map_section, r"[ \.#]", str_processor).items()
            if v != " "
        }
        self.instructions = split(
            r"(L|R)",
            parse_single_line(directions_section, r"[0-9LR]+", str_processor),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        # count the number of rows and columns in the net
        cols, rows = ((max(a) + 1) for a in zip(*self.map))

        # find the min and max extend of the net
        row_min = [maxsize for y in range(rows)]
        row_max = [0 for y in range(rows)]
        col_min = [maxsize for x in range(cols)]
        col_max = [0 for x in range(cols)]
        for x, y in self.map:
            row_min[y] = min(row_min[y], x)
            row_max[y] = max(row_max[y], x)
            col_min[x] = min(col_min[x], y)
            col_max[x] = max(col_max[x], y)

        # navigate the net, wrapping at the edges
        x, y = min((x, y) for x, y in self.map if y == 0)
        direction = 0
        turn = {"L": -1, "R": 1}
        for instruction in self.instructions:
            if instruction in turn:
                direction = (direction + turn[instruction]) % 4
            else:
                for _ in range(int(instruction)):
                    x1, y1 = [
                        ((x + 1) if x < row_max[y] else row_min[y], y),
                        (x, (y + 1) if y < col_max[x] else col_min[x]),
                        ((x - 1) if x > row_min[y] else row_max[y], y),
                        (x, (y - 1) if y > col_min[x] else col_max[x]),
                    ][direction]
                    if self.map[(x1, y1)] == ".":
                        x, y = x1, y1
                    else:
                        break
        return self._password(x, y, direction)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # find the length of the sides of the cube
        side = int(sqrt(len(self.map) / 6))

        # cube is array which holds the spaces/walls (just ignore the empty middle)
        # each face will have a boarder of -1 around, to assist with cube rotations
        cube = np.full((side + 2, side + 2, side + 2), -1, dtype=np.int_)

        # tracker holds the original (x,y) of the net, which will be rotated
        # around in sync with the cube, to make life easier at the end
        tracker = np.zeros(
            (side + 2, side + 2, side + 2), dtype=[("x", np.int_), ("y", np.int_)]
        )

        # compass holds the orientation of the net, rotated in sync with tracker
        compass = np.full((5, 5, 5), -1, dtype=np.int_)

        # start at the top left of the net
        start_x, start_y = min((x, y) for x, y in self.map if y == 0)

        # use a breadth first search to exploe the net, rolling the cube around
        # to map the net onto the cuve
        queue = deque([(start_x, start_y, cube, tracker, compass)])
        visited = {(start_x, start_y)}
        while queue:
            net_x, net_y, cube_view, tracker_view, compass_view = queue.popleft()

            # copy the net onto the face of the cube,
            # then update the tracker and compass
            cube_view[0, 1 : side + 1, 1 : side + 1] = np.array(
                [
                    [self.map[(net_x + x, net_y + y)] == "." for x in range(side)]
                    for y in range(side)
                ]
            )
            tracker_view[0, 1 : side + 1, 1 : side + 1] = np.array(
                [[(net_x + x, net_y + y) for x in range(side)] for y in range(side)],
                dtype=[("x", np.int_), ("y", np.int_)],
            )
            compass_view[0, 1:4, 1:4] = np.array(
                [[-1, 3, -1], [2, 100, 0], [-1, 1, -1]]
            )

            # explore a path through the net, rolling the cube as we go, so that
            # we can copy the net onto the front face of the cube
            moves = [
                (net_x + side, net_y, (0, 2)),  # right
                (net_x, net_y + side, (0, 1)),  # down
                (net_x - side, net_y, (2, 0)),  # left
                (net_x, net_y - side, (1, 0)),  # up
            ]
            for x, y, axis in moves:
                if (x, y) in self.map and (x, y) not in visited:
                    visited.add((x, y))
                    queue.append(
                        (
                            x,
                            y,
                            np.rot90(cube_view, 1, axis),
                            np.rot90(tracker_view, 1, axis),
                            np.rot90(compass_view, 1, axis),
                        )
                    )

        # now, follow the movement instructions, rotating the cube so that
        # we are always moving around the front face of the cube
        x, y = 1, 1
        direction = 0
        turn = {"L": -1, "R": 1}
        for instruction in self.instructions:
            if instruction in turn:
                # make the turn
                direction = (direction + turn[instruction]) % 4
            else:
                for _ in range(int(instruction)):
                    # move forward one step
                    y1, x1, axis, y2, x2 = [
                        (y, x + 1, (0, 2), y, 1),
                        (y + 1, x, (0, 1), 1, x),
                        (y, x - 1, (2, 0), y, side),
                        (y - 1, x, (1, 0), side, x),
                    ][direction]

                    if cube[0][y1][x1] == 1:
                        # can move forward one step with rotating the cube
                        y, x = y1, x1
                    elif cube[0][y1][x1] == 0:
                        # moving forward will hit a wall, so stop moving
                        break
                    else:
                        # rotate cube, to see if we can move forward
                        rotated_cube = np.rot90(cube, 1, axis)
                        if rotated_cube[0][y2][x2] == 1:
                            # can move forward having rotated the cube
                            cube = rotated_cube
                            tracker = np.rot90(tracker, 1, axis)
                            compass = np.rot90(compass, 1, axis)
                            y, x = y2, x2
                        else:
                            # a wall is blocking the movement
                            break

        # use the tracker to reverse map from cube to net,
        # then find the direction from the compass
        net_x, net_y = tracker[0][y][x]
        net_direction = [
            compass[0][2][3],
            compass[0][3][2],
            compass[0][2][1],
            compass[0][1][2],
        ][direction]

        # generate the password
        return self._password(net_x, net_y, net_direction)

    def _password(self, x: int, y: int, direction: int) -> int:
        """Generate the password.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            direction (int): direction of travel

        Returns:
            int: the numeric password
        """
        return (1000 * (y + 1)) + (4 * (x + 1)) + direction % 4


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
