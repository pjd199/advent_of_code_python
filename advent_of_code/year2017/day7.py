"""Solves the puzzle for Day 7 of Advent of Code 2017.

Recursive Circus

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/7
"""
from dataclasses import dataclass, field
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 7
    TITLE = "Recursive Circus"

    @dataclass
    class _Program:
        name: str
        weight: int
        contents: str = ""
        disc: List["Solver._Program"] = field(default_factory=list)

        def total_weight(self) -> int:
            return self.weight + sum(x.total_weight() for x in self.disc)

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = {
            x.name: x
            for x in parse_lines(
                puzzle_input,
                (
                    r"(?P<name>\w+) \((?P<weight>\d+)\)"
                    r"( -> (?P<contents>(\w+(, )?)+))?",
                    dataclass_processor(Solver._Program),
                ),
            )
        }
        for program in self.input.values():
            if program.contents:
                program.disc = [self.input[x] for x in program.contents.split(", ")]
        self.root = ""

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        possible = {program.name for program in self.input.values() if program.disc}
        held = {
            x.name
            for program in self.input.values()
            for x in program.disc
            if program.disc
        }
        self.root = list(possible.difference(held))[0]
        return self.root

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if self.root == "":
            self.solve_part_one()

        # find where the mistake is
        program = self.input[self.root]
        path = [program]
        while program.disc:
            weights = [x.total_weight() for x in program.disc]
            if all(x == y for x, y in zip(weights, weights[1:])):
                break
            else:
                program = program.disc[
                    weights.index(min(set(weights), key=weights.count))
                ]
                path.append(program)

        # find the correct weight
        weights = [x.total_weight() for x in path[-2].disc]
        return path[-1].weight + (
            max(set(weights), key=weights.count) - min(set(weights), key=weights.count)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
