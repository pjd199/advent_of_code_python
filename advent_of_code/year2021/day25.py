"""Solves the puzzle for Day 25 of Advent of Code 2021.

Sea Cucumber

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/25
"""
from copy import deepcopy
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 25
    TITLE = "Sea Cucumber"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(puzzle_input, (r"[>v.]", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        grid = deepcopy(self.input)

        def move(movements: list[tuple[tuple[int, int], tuple[int, int]]]) -> bool:
            for (x1, y1), (x2, y2) in movements:
                grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]
            return len(movements) > 0

        cycles = 0
        changed = True
        while changed:
            # move all the ">"
            changed = move(
                [
                    (((x - 1) % len(row), y), (x, y))
                    for y, row in enumerate(grid)
                    for x, (current, previous) in enumerate(zip(row, row[-1:] + row))
                    if current == "." and previous == ">"
                ]
            )
            # move all the "v"
            changed |= move(
                [
                    ((x, (y - 1) % len(grid)), (x, y))
                    for y, (current_row, previous_row) in enumerate(
                        zip(grid, grid[-1:] + grid)
                    )
                    for x in range(len(current_row))
                    if current_row[x] == "." and previous_row[x] == "v"
                ]
            )
            cycles += 1

        return cycles

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: But can never do it!
        Raises:
            NotImplementedError: always!
        """
        raise NotImplementedError("No part two on Christmas Day!!!")


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
