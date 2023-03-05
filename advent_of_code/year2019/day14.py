"""Solves the puzzle for Day 14 of Advent of Code 2019.

Space Stoichiometry

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/14
"""
from collections import defaultdict
from math import ceil
from pathlib import Path
from sys import path
from typing import DefaultDict, List, Set

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    parse_lines,
    parse_tokens_single_line,
    str_tuple_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 14
    TITLE = "Space Stoichiometry"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.reactions = {
            out: (
                int(quantity),
                parse_tokens_single_line(
                    [in_list],
                    (r"([0-9]+) ([A-Z]+)", lambda m: (int(m[1]), m[2])),
                    delimiter=r", ",
                    require_delimiter=False,
                ),
            )
            for in_list, quantity, out in parse_lines(
                puzzle_input,
                (
                    r"(?P<in_list>[0-9A-Z, ]+) => (?P<quantity>[0-9]+) (?P<out>[A-Z]+)",
                    str_tuple_processor,
                ),
            )
        }
        self.topo: List[str] = []

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.prepare_to_solve()
        return self.ore_requirements(1)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self.prepare_to_solve()

        # perform a binary search to find the maximum fuel that can be made
        # given the specified ammount of useable ore
        useable_ore = 1000000000000
        lower = 1
        upper = useable_ore
        while (upper - lower) > 1:
            middle = (upper + lower) // 2
            ore = self.ore_requirements(middle)
            if ore <= useable_ore:
                lower = middle
            if ore >= useable_ore:
                upper = middle

        return lower

    def prepare_to_solve(self) -> None:
        """Prepare to solve."""
        # only need to do the topological sort once
        if self.topo:
            return

        # work out all the dependencies in the reactions
        dependancies: DefaultDict[str, Set[str]] = defaultdict(set)
        dependancies["ORE"]
        for chemical, (_, ingredients) in self.reactions.items():
            dependancies[chemical].update({x for _, x in ingredients})

        # perform a topological sorting algorithm
        visited: Set[str] = set()
        while len(visited) < len(dependancies):
            # find the chemicals with no dependancies
            zero_dependancies = {
                chemical
                for chemical, dependancy in dependancies.items()
                if not dependancy and chemical not in visited
            }
            # add zero dependancies to the topo list and mark as visited
            self.topo.extend(zero_dependancies)
            visited.update(zero_dependancies)

            # clear the visited chemicals from each dependancy list
            for dependancy in dependancies.values():
                dependancy.difference_update(zero_dependancies)

    def ore_requirements(self, units_of_fuel: int) -> int:
        """Calculate the ORE requirement for the requests units of FUEL.

        Args:
            units_of_fuel (int): how much FUEL

        Returns:
            int: ORE needed
        """
        needs: DefaultDict[str, int] = defaultdict(int)
        needs["FUEL"] = units_of_fuel

        # traverse the reactions in topological order, recording the total quanity
        # of each chemical needed as you go
        for chemical in (x for x in reversed(self.topo) if x != "ORE"):
            need = needs[chemical]
            produces, ingredients = self.reactions[chemical]
            factor = ceil(need / produces)
            for ammount, ingredient in ingredients:
                needs[ingredient] += factor * ammount

        return needs["ORE"]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
