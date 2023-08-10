"""Solves the puzzle for Day 11 of Advent of Code 2022.

Monkey in the Middle

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/11
"""
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass, field
from math import prod
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, split_sections, str_processor_group
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class _Monkey:
    """A Monkey from the puzzle input."""

    items: list[int]
    operator: str
    op_value: int
    test: int
    throw: dict[bool, int]
    inspections: int = field(default=0)


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 11
    TITLE = "Monkey in the Middle"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.monkeys: list[_Monkey] = []
        for section in split_sections(puzzle_input):
            lines = parse_lines(
                section,
                (r"Monkey (\d+):", str_processor_group(1)),
                (r"  Starting items: ([0-9, ]+)", str_processor_group(1)),
                (r"  Operation: new = old ([+*] (\d+|old))", str_processor_group(1)),
                (r"  Test: divisible by (\d+)", str_processor_group(1)),
                (r"    If true: throw to monkey (\d+)", str_processor_group(1)),
                (r"    If false: throw to monkey (\d+)", str_processor_group(1)),
            )
            op, value = lines[2].split(" ")
            self.monkeys.append(
                _Monkey(
                    [int(x) for x in lines[1].split(", ")],
                    "square" if value == "old" else op,
                    int(value) if value != "old" else -1,
                    int(lines[3]),
                    {True: int(lines[4]), False: int(lines[5])},
                )
            )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(20, lambda x: x // 3)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        modulo = prod(x.test for x in self.monkeys)
        return self._solve(10000, lambda x: x % modulo)

    def _solve(self, rounds: int, worry_reducer: Callable[[int], int]) -> int:
        """Solve the puzzle.

        Args:
            rounds (int): the number of rounds to play
            worry_reducer (Callable[[int], int]): function for reducing worry levels

        Returns:
            int: the result
        """
        monkeys = deepcopy(self.monkeys)

        op: dict[str, Callable[[int, int], int]] = {
            "*": lambda old, value: old * value,
            "+": lambda old, value: old + value,
            "square": lambda old, value: old * old,
        }

        # play the rounds
        for _ in range(rounds):
            for monkey in monkeys:
                for item in monkey.items:
                    level = op[monkey.operator](item, monkey.op_value)
                    level = worry_reducer(level)
                    throw_to = monkey.throw[level % monkey.test == 0]
                    monkeys[throw_to].items.append(level)
                monkey.inspections += len(monkey.items)
                monkey.items.clear()

        # find the product of the two top passing monkeys
        return prod(sorted((x.inspections for x in monkeys))[-2:])


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
