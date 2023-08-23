"""Solves the puzzle for Day 3 of Advent of Code 2021.

Binary Diagnostic

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/3
"""
from collections import Counter
from operator import itemgetter
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 3
    TITLE = "Binary Diagnostic"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[01]+", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        counters = [
            Counter(x[i] for x in self.input) for i in range(len(self.input[0]))
        ]
        counts = [sorted(counter.items(), key=itemgetter(1)) for counter in counters]
        most_common = "".join([x[1][0] for x in counts])
        least_common = "".join([x[0][0] for x in counts])
        return int(most_common, 2) * int(least_common, 2)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        def find(values: set[str], target: bool, index: int = 0) -> int:
            # target : least common = False, most common = True
            if len(values) == 1:
                return int(values.pop(), 2)

            counter = Counter(x[index] for x in values)
            counts = sorted(counter.items(), key=itemgetter(1))
            if len(counts) > 1 and counts[0][1] == counts[1][1]:
                common = "0" if target else "1"
            else:
                common = counts[(0 if target else -1)][0]
            return find({x for x in values if x[index] == common}, target, index + 1)

        oxygen_rating = find(set(self.input), False)
        co2_rating = find(set(self.input), True)
        return oxygen_rating * co2_rating


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
