"""Solves the puzzle for Day 5 of Advent of Code 2023.

If You Give A Seed A Fertilizer

For puzzle specification and desciption, visit
https://adventofcode.com/2023/day/5
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    int_processor,
    int_tuple_processor,
    parse_lines,
    parse_single_line,
    parse_tokens_single_line,
    split_sections,
    str_processor_group,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2023
    DAY = 5
    TITLE = "If You Give A Seed A Fertilizer"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        # split the input file into sections
        sections = split_sections(puzzle_input, expected_sections=8)

        # parse the seed section
        self.seeds = parse_tokens_single_line(
            parse_lines(sections[0], (r"seeds: ([\d+ ]*)", str_processor_group(1))),
            (r"\d+", int_processor),
            delimiter=" ",
        )

        # parse other sections into categories and maps
        self.categories = {}
        self.maps = {}
        for section in sections[1:]:
            source, destination = parse_single_line(
                section[:1], r"([a-z]+)-to-([a-z]+) map:", str_tuple_processor
            )
            self.categories[source] = destination
            self.maps[source] = parse_lines(
                section[1:], (r"(\d+) (\d+) (\d+)", int_tuple_processor)
            )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self.solve([(x, 1) for x in self.seeds])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self.solve(list(zip(self.seeds[0::2], self.seeds[1::2])))

    def solve(self, ranges: list[tuple[int, int]]) -> int:
        """Solve the problem.

        Args:
            ranges (list[tuple[int, int]]): the seed ranges to process

        Returns:
            int: the lowest location number at the end
        """
        category = "seed"
        while category != "location":
            # find the breakpoint markers for this category
            markers = []
            for _, src, length in self.maps[category]:
                markers.append(src)
                markers.append(src + length - 1)
            markers.sort()

            # break up the ranges
            modified_ranges = []
            for number, span in ranges:
                broken = False
                for marker in markers:
                    if number <= marker < number + span:
                        modified_ranges.append((number, marker - number))
                        span = span - (marker - number)
                        number = marker
                        broken = True
                if not broken or span > 0:
                    modified_ranges.append((number, span))

            # map the ranges, which will now all fit within a mapping
            next_ranges = []
            for number, span in modified_ranges:
                for dest, src, length in self.maps[category]:
                    if src <= number < src + length:
                        number = number - src + dest
                        break
                next_ranges.append((number, span))

            # advance to the next level
            ranges = next_ranges
            category = self.categories[category]

        return min(x for x, _ in ranges)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
