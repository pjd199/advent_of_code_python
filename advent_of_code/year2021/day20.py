"""Solves the puzzle for Day 20 of Advent of Code 2021.

Trench Map

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/20
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_grid,
    parse_tokens_single_line,
    split_sections,
    str_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 20
    TITLE = "Trench Map"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input)
        self.algorithm = parse_tokens_single_line(sections[0], (r"[#.]", str_processor))
        self.image = parse_grid(sections[1], r"[.#]", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(2)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(50)

    def _solve(self, cycles: int) -> int:

        # try speeds with lists and numpy

        infinite_pixel = "."
        image = self.image.copy()
        for _ in range(cycles):
            (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*image))
            image = {
                (x, y): self.algorithm[
                    int(
                        "".join(
                            [
                                "1" if image.get(p, infinite_pixel) == "#" else "0"
                                for p in [
                                    (x - 1, y - 1),
                                    (x, y - 1),
                                    (x + 1, y - 1),
                                    (x - 1, y),
                                    (x, y),
                                    (x + 1, y),
                                    (x - 1, y + 1),
                                    (x, y + 1),
                                    (x + 1, y + 1),
                                ]
                            ]
                        ),
                        base=2,
                    )
                ]
                for y in range(min_y - 1, max_y + 2)
                for x in range(min_x - 1, max_x + 2)
            }
            infinite_pixel = (
                self.algorithm[0] if infinite_pixel == "." else self.algorithm[511]
            )
        return sum(1 for p in image.values() if p == "#")


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
