"""Solves the puzzle for Day 12 of Advent of Code 2020.

Rain Risk

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/12
"""
from collections.abc import Callable
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 12
    TITLE = "Rain Risk"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        #         puzzle_input = """F10
        # N3
        # F7
        # R90
        # F11""".splitlines()
        self.input = [
            (x, int(y))
            for x, y in parse_lines(
                puzzle_input, (r"([NESWLRF])(\d+)", str_tuple_processor)
            )
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        x, y = 0, 0
        direction = 90

        for command, value in self.input:
            if command == "N" or (command == "F" and direction == 0):
                y -= value
            elif command == "E" or (command == "F" and direction == 90):
                x += value
            elif command == "S" or (command == "F" and direction == 180):
                y += value
            elif command == "W" or (command == "F" and direction == 270):
                x -= value
            elif command == "L":
                direction = (direction - value) % 360
            elif command == "R":
                direction = (direction + value) % 360

        return abs(x) + abs(y)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        ship_x, ship_y = 0, 0
        waypoint_x, waypoint_y = 10, -1

        rotate: dict[str, dict[int, Callable[[int, int], tuple[int, int]]]] = {
            "L": {
                90: lambda x, y: (y, -x),
                180: lambda x, y: (-x, -y),
                270: lambda x, y: (-y, x),
            },
            "R": {
                90: lambda x, y: (-y, x),
                180: lambda x, y: (-x, -y),
                270: lambda x, y: (y, -x),
            },
        }

        move: dict[str, Callable[[int, int, int], tuple[int, int]]] = {
            "N": lambda x, y, v: (x, y - v),
            "E": lambda x, y, v: (x + v, y),
            "S": lambda x, y, v: (x, y + v),
            "W": lambda x, y, v: (x - v, y),
        }

        for command, value in self.input:
            if command in "NESW":
                waypoint_x, waypoint_y = move[command](waypoint_x, waypoint_y, value)
            elif command in "LR":
                waypoint_x, waypoint_y = rotate[command][value](waypoint_x, waypoint_y)
            elif command == "F":
                ship_x += value * waypoint_x
                ship_y += value * waypoint_y

        return abs(ship_x) + abs(ship_y)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
