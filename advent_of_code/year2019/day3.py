"""Solves the puzzle for Day 3 of Advent of Code 2019.

Crossed Wires

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/3
"""
from collections.abc import Callable
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 3
    TITLE = "Crossed Wires"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input, (r"[URDL]\d+", str_processor), delimiter=","
        )
        self.wires_mapped = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._map_wires()
        return min(abs(x) + abs(y) for x, y in self.intersections)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._map_wires()
        dist_a, dist_b = (
            {
                (x, y): len(wire) - i - 1
                for i, (x, y) in enumerate(reversed(wire))
                if (x, y) in self.intersections
            }
            for wire in [self.wire_a, self.wire_b]
        )
        return min(dist_a[(x, y)] + dist_b[(x, y)] for x, y in self.intersections)

    def _map_wires(self) -> None:
        """Prepare the wires."""
        if not self.wires_mapped:
            self.wire_a, self.wire_b = [self._draw_wire(x) for x in self.input]
            self.intersections = set(self.wire_a) & set(self.wire_b) - {(0, 0)}
            self.wires_mapped = True

    def _draw_wire(self, path: list[str]) -> list[tuple[int, int]]:
        """Draw the wires, point by point.

        Args:
            path (list[str]): the path to follow

        Returns:
            list[tuple[int, int]]: the result
        """
        draw_line: dict[str, Callable[[int, int, int], list[tuple[int, int]]]] = {
            "U": lambda x, y, d: [(x, y - delta) for delta in range(1, d + 1)],
            "R": lambda x, y, d: [(x + delta, y) for delta in range(1, d + 1)],
            "D": lambda x, y, d: [(x, y + delta) for delta in range(1, d + 1)],
            "L": lambda x, y, d: [(x - delta, y) for delta in range(1, d + 1)],
        }

        result: list[tuple[int, int]] = [(0, 0)]
        for point in path:
            direction = point[0]
            distance = int(point[1:])
            result.extend(draw_line[direction](*result[-1], distance))

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
