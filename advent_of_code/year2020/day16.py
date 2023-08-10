"""Solves the puzzle for Day 16 of Advent of Code 2020.

Ticket Translation

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/16
"""
from dataclasses import dataclass, field
from itertools import chain
from math import prod
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    dataclass_processor,
    int_processor,
    parse_lines,
    parse_tokens,
    split_sections,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Rule:
    """A rule from the input."""

    name: str
    a_min: int
    a_max: int
    b_min: int
    b_max: int
    valid: set[int] = field(default_factory=set)


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 16
    TITLE = "Ticket Translation"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input, expected_sections=3)
        self.rules = parse_lines(
            sections[0],
            (
                r"(?P<name>[\w\- ]+): (?P<a_min>\d+)-(?P<a_max>\d+) or "
                r"(?P<b_min>\d+)-(?P<b_max>\d+)",
                dataclass_processor(Rule),
            ),
        )
        self.ticket = parse_tokens(
            sections[1],
            (r"\d+", int_processor),
            delimiter=",",
            header=("your ticket:",),
            min_length=1,
            max_length=2,
        )[0]
        self.nearby = parse_tokens(
            sections[2],
            (r"\d+", int_processor),
            delimiter=",",
            header=("nearby tickets:",),
            min_length=2,
        )
        self.ready_to_solve = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._prepare_to_solve()
        return sum(x for ticket in self.nearby for x in ticket if x not in self.valid)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._prepare_to_solve()
        # remove the invalid tickets
        invalid_tickets = {
            i
            for i, ticket in enumerate(self.nearby)
            for value in ticket
            if value not in self.valid
        }

        tickets = [
            ticket for i, ticket in enumerate(self.nearby) if i not in invalid_tickets
        ]

        # transpose the data from into columns
        columns = [
            {ticket[order] for ticket in tickets} for order in range(len(self.rules))
        ]

        # find the possibilities
        possible = [
            {rule.name for rule in self.rules if column <= rule.valid}
            for column in columns
        ]

        # find the actual matches, by searching for possibilities with just
        # one value, then removing them
        actual = {}
        while any(x for x in possible):
            # find singles
            for i in range(len(possible)):
                if len(possible[i]) == 1:
                    found = possible[i].pop()
                    actual[i] = found
                    for x in possible:
                        if found in x:
                            x.remove(found)

        return prod(self.ticket[i] for i, name in actual.items() if "departure" in name)

    def _prepare_to_solve(self) -> None:
        """Expand the rules into sets of int."""
        if not self.ready_to_solve:
            for rule in self.rules:
                rule.valid = set(
                    chain(
                        range(rule.a_min, rule.a_max + 1),
                        range(rule.b_min, rule.b_max + 1),
                    )
                )
            self.valid = set().union(*[rule.valid for rule in self.rules])
            self.ready_to_solve = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
