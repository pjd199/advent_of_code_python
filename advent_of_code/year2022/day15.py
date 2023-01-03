"""Solves the puzzle for Day 15 of Advent of Code 2022.

Beacon Exclusion Zone

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/15
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 15
    TITLE = "Beacon Exclusion Zone"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                r"Sensor at x=(-?\d+), y=(-?\d+): "
                r"closest beacon is at x=(-?\d+), y=(-?\d+)",
                int_tuple_processor,
            ),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        target_y = 2000000
        ranges = []
        beacons = set()
        for sensor_x, sensor_y, beacon_x, beacon_y in self.input:
            dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            if beacon_y == target_y:
                beacons.add(beacon_x)

            if abs(sensor_y - target_y) <= dist:
                offset = dist - abs(sensor_y - target_y)
                ranges.append((sensor_x - offset, sensor_x + offset + 1))

        ranges.sort()
        result = 0
        last = ranges[0][0] - 1
        for a, b in ranges:
            if a > last:
                result += b - a
                if any(a <= beacon <= b for beacon in beacons):
                    result -= 1
                last = b
            if b > last:
                result += b - last
                last = b

        return result

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        limit = 4000000
        result = -1
        found = False
        for y in range(limit):
            ranges = []
            for sensor_x, sensor_y, beacon_x, beacon_y in self.input:
                dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

                if abs(sensor_y - y) <= dist:
                    offset = dist - abs(sensor_y - y)
                    ranges.append((sensor_x - offset, sensor_x + offset))

            ranges.sort()
            last = ranges[0][0] - 1
            for a, b in ranges:
                if a > last:
                    if a - last == 2:
                        result = ((last + 1) * 4000000) + y
                        found = True
                    last = b
                if b > last:
                    last = b
            if found:
                break

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
