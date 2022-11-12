"""Solves the puzzle for Day 7 of Advent of Code 2018.

The Sum of Its Parts

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/7
"""
from collections import defaultdict
from itertools import chain
from pathlib import Path
from sys import path
from typing import Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 7
    TITLE = "The Sum of Its Parts"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        lines = parse_lines(
            puzzle_input,
            (
                r"Step (?P<a>[A-Z]) must be finished before step "
                r"(?P<b>[A-Z]) can begin.",
                str_tuple_processor,
            ),
        )
        self.steps = defaultdict(list)
        for a, b in lines:
            self.steps[a].append(b)

        self.dependencies = defaultdict(list)
        for a, b in lines:
            self.dependencies[b].append(a)

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        result = []
        pool = set(self.steps.keys()) - set(chain.from_iterable(self.steps.values()))
        complete = set()

        while pool:
            for step in sorted(pool):
                if all(x in complete for x in self.dependencies[step]):
                    pool.remove(step)
                    if step not in complete:
                        result.append(step)
                        complete.add(step)
                    pool.update(self.steps[step])
                    break

        return "".join(result)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        result = []
        pool = set(self.steps.keys()) - set(chain.from_iterable(self.steps.values()))
        working: Dict[str, int] = {}
        complete = set()
        tick = -1

        while pool or working:
            tick += 1

            new_working = {}
            for step, value in working.items():
                if value > 0:
                    new_working[step] = value - 1
                else:
                    result.append(step)
                    complete.add(step)
            working = new_working

            for step in sorted(pool):
                if len(working) < 5 and (
                    all(x in complete for x in self.dependencies[step])
                ):
                    pool.remove(step)
                    if step not in complete and step not in working:
                        working[step] = 60 + (ord(step) - ord("A"))
                    pool.update(self.steps[step])

        return tick


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
