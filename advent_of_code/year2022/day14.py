"""Solves the puzzle for Day 14 of Advent of Code 2022.

Regolith Reservoir

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/14
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 14
    TITLE = "Regolith Reservoir"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_tokens(
            puzzle_input,
            (r"(\d+),(\d+)", lambda m: (int(m[1]), int(m[2]))),
            delimiter=" -> ",
        )
        self.origin = (500, 0)
        self.rocks = {
            (x, y)
            for line in self.input
            for (x1, y1), (x2, y2) in zip(line, line[1:])
            for x in range(min(x1, x2), max(x1, x2) + 1)
            for y in range(min(y1, y2), max(y1, y2) + 1)
        }

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        max_y = max(y for _, y in self.rocks)

        # simulate sand particles, falling one by one
        filled = set(self.rocks)
        y = 0
        while y <= max_y:
            x, y = self.origin
            while y <= max_y:
                if (x, y + 1) not in filled:
                    y += 1
                elif (x - 1, y + 1) not in filled:
                    x -= 1
                    y += 1
                elif (x + 1, y + 1) not in filled:
                    x += 1
                    y += 1
                else:
                    filled.add((x, y))
                    break

        return len(filled - self.rocks)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        max_y = max(y for _, y in self.rocks)

        # find all the possible locations for sand, line by line
        # which is more effecient than simulating individual grains of sand
        previous = {self.origin}
        count = 1

        for y in range(1, max_y + 2):
            current = {
                (x1, y)
                for x, _ in previous
                for x1 in range(x - 1, x + 2)
                if (x1, y) not in self.rocks
            }
            count += len(current)
            previous = current

        return count


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
