"""Solves the puzzle for Day 4 of Advent of Code 2018.

Repose Record

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/4
"""
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from sys import path
from typing import Counter as CounterType
from typing import DefaultDict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, enum_re, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class Action(Enum):
    """Action from the puzzle input."""

    BEGIN = "begins shift"
    WAKE = "wakes up"
    SLEEP = "falls asleep"


@dataclass(order=True)
class Event:
    """Event line from the puzzle input."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    action: Action
    identifier: int = -1


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 4
    TITLE = "Repose Record"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                rf"\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) "
                rf"(?P<hour>\d+):(?P<minute>\d+)\] "
                rf"(Guard #(?P<identifier>\d+) )?"
                rf"(?P<action>{enum_re(Action)})",
                dataclass_processor(Event),
            ),
        )
        self.guards: DefaultDict[int, CounterType[int]] = defaultdict(Counter)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.guards:
            self.count()

        # find sleepiest guard
        longest = -1
        guard = -1
        for identifier, pattern in self.guards.items():
            length = sum(pattern.values())
            if length > longest:
                longest = length
                guard = identifier

        return guard * self.guards[guard].most_common(1)[0][0]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.guards:
            self.count()

        # find the gaurd with the sleepiest minute
        highest_frequency = -1
        highest_minute = -1
        guard = -1
        for identifier in self.guards.keys():
            minute, frequency = self.guards[identifier].most_common(1)[0]
            if frequency > highest_frequency:
                highest_frequency = frequency
                highest_minute = minute
                guard = identifier

        return guard * highest_minute

    def count(self) -> None:
        """Count the times the guards sleep."""
        # Create a mapping of guard identifier to a counter of time(minute) when asleep
        guard = -1
        start = -1

        for event in sorted(self.input):
            if event.action == Action.BEGIN:
                guard = event.identifier
            elif event.action == Action.SLEEP:
                start = event.minute
            elif event.action == Action.WAKE:
                self.guards[guard].update(range(start, event.minute))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
