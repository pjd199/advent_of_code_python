"""Solves the puzzle for Day 17 of Advent of Code 2022.

Pyroclastic Flow

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/17
"""
from pathlib import Path
from sys import path
from typing import Callable, List, Set, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 17
    TITLE = "Pyroclastic Flow"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(
            puzzle_input,
            (r"[<>]", str_processor),
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        values = self._solve(2022)
        return abs(values[-1][3])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        target = 1000000000000
        values = self._solve(4000)

        # find the start of the repeating pattern
        period = 1
        while values[-1][:3] != values[-1 - period][:3]:
            period += 1

        cycle = values[-period:]
        cycle_index = (target - len(values)) % len(cycle)
        added_height = abs(
            ((target - len(values)) // len(cycle)) * (cycle[-1][3] - cycle[0][3] - 1)
        )

        return abs(
            values[-1][3] - added_height - abs(cycle[cycle_index][3] - cycle[0][3])
        )

    def _solve(self, rock_count: int) -> List[Tuple[int, int, int, int]]:
        """Solve  the puzzle.

        Args:
            rock_count (int): the number of falling rocks to count

        Returns:
            List[Tuple[int, int, int, int]]: the state for each rock
        """
        # define each shape - positive co-ordinates are left/down,
        # so height from floor is measured as a negative
        shape_functions: List[Callable[[int], Set[Tuple[int, int]]]] = [
            # "-" shape
            lambda y: {(2, y), (3, y), (4, y), (5, y)},
            # "+" shape
            lambda y: {
                (3, y - 2),
                (2, y - 1),
                (3, y - 1),
                (4, y - 1),
                (3, y),
            },
            # reverse "L" shape
            lambda y: {
                (4, y - 2),
                (4, y - 1),
                (2, y),
                (3, y),
                (4, y),
            },
            # "I" shape
            lambda y: {(2, y - 3), (2, y - 2), (2, y - 1), (2, y)},
            # "." shape
            lambda y: {(2, y - 1), (3, y - 1), (2, y), (3, y)},
        ]

        # define location of the floor in the set of solid rock
        solid = {(x, 0) for x in range(7)}

        shape_index = 0
        wind_index = 0

        values = []

        for _ in range(rock_count):
            top = min(y for _, y in solid)

            rock = shape_functions[shape_index](top - 4)
            shape_index = (shape_index + 1) % len(shape_functions)
            while True:
                # move left or right in a jet of air, if we can
                move = -1 if self.input[wind_index] == "<" else 1
                wind_index = (wind_index + 1) % len(self.input)

                moved_rock = {(x + move, y) for x, y in rock}
                if all(0 <= x < 7 for x, _ in moved_rock) and not moved_rock & solid:
                    rock = moved_rock

                # move down, if we can
                moved_rock = {(x, y + 1) for x, y in rock}
                if moved_rock & solid:
                    solid.update(rock)

                    # store the result
                    top = min(y for _, y in solid)
                    row = sum(1 << x for x in range(7) if (x, top) in solid)
                    values.append((shape_index, wind_index, row, top))

                    break
                else:
                    rock = moved_rock

        return values


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
