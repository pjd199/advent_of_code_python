"""Solves the puzzle for Day 11 of Advent of Code 2020.

Seating System

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/11
"""
from itertools import count
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 11
    TITLE = "Seating System"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[.L]", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        seats = {(x, y): False for (x, y), v in self.input.items() if v == "L"}

        finished = False
        while not finished:
            next_seats = {}
            for x, y in seats:
                adjacent = sum(
                    1
                    for x1, y1 in [
                        (x - 1, y - 1),
                        (x, y - 1),
                        (x + 1, y - 1),
                        (x - 1, y),
                        (x + 1, y),
                        (x - 1, y + 1),
                        (x, y + 1),
                        (x + 1, y + 1),
                    ]
                    if seats.get((x1, y1), False)
                )
                if seats[(x, y)]:
                    next_seats[(x, y)] = adjacent < 4
                else:
                    next_seats[(x, y)] = adjacent == 0

            finished = seats == next_seats
            seats = next_seats

        return sum(1 for x in seats.values() if x)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        seats = {(x, y): False for (x, y), v in self.input.items() if v == "L"}
        (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*seats))

        finished = False
        next_seats: dict[tuple[int, int], bool] = {}
        while not finished:
            next_seats = {}
            for x, y in seats:
                adjacent = 0
                looks = [
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                    (-1, 0),
                    (1, 0),
                    (-1, 1),
                    (0, 1),
                    (1, 1),
                ]
                for x_delta, y_delta in looks:
                    for i in count(1):
                        x1, y1 = (x + (x_delta * i), y + (y_delta * i))
                        if min_x <= x1 <= max_x and min_y <= y1 <= max_y:
                            if (x1, y1) in seats:
                                adjacent += 1 if seats[(x1, y1)] else 0
                                break
                        else:
                            break

                if seats[(x, y)]:
                    next_seats[(x, y)] = adjacent < 5
                else:
                    next_seats[(x, y)] = adjacent == 0

            finished = seats == next_seats
            seats = next_seats

        return sum(1 for x in seats.values() if x)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
