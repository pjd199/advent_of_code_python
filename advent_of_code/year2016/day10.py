"""Solves the puzzle for Day 10 of Advent of Code 2016.

Balance Bots

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from abc import ABC
from math import prod
from pathlib import Path
from sys import path
from typing import Callable, Dict, List, Tuple, cast

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 10
    TITLE = "Balance Bots"

    class _ChipPassingProtocol(ABC):
        """Parent of _OutputBin and _Robot classes."""

        def __init__(self, identifier: str) -> None:
            """Initialise the item.

            Args:
                identifier (str): The identifier string
            """
            self.identifier = identifier
            self.chips: List[int] = []

        def add_chip(self, value: int) -> None:
            """Add a chip to the item.

            Args:
                value (int): the chip's value
            """
            self.chips.append(value)
            self.chips.sort()

        def __str__(self) -> str:
            """The identifier for the object.

            Returns:
                str: the identifier of the item
            """
            return self.identifier

    class _OutputBin(_ChipPassingProtocol):
        """An Output Bin."""

        pass

    class _Robot(_ChipPassingProtocol):
        """A Robot."""

        def __init__(
            self,
            identifier: str,
            giving_callback: Callable[["Solver._Robot"], None],
        ) -> None:
            """Initialise the Robot with an indentifier and logger.

            Args:
                identifier (str): The robot's identifier
                giving_callback (Callable[[&quot;Solver._Robot&quot;], None]): called
                    when values are given away
            """
            super().__init__(identifier)
            self.giving_callback = giving_callback

        def instruction(
            self,
            low_goes_to: "Solver._ChipPassingProtocol",
            high_goes_to: "Solver._ChipPassingProtocol",
        ) -> None:
            """Add the instruction to the Robot.

            Args:
                low_goes_to (Solver._ChipPassingProtocol): low value receiver
                high_goes_to (Solver._ChipPassingProtocol): high value receiver
            """
            self.low_goes_to = low_goes_to
            self.high_goes_to = high_goes_to

        def add_chip(self, value: int) -> None:
            """Add a chip to the robot, and execute instruction if have two chips.

            Args:
                value (int): the value to add
            """
            super().add_chip(value)
            if len(self.chips) == 2:
                self.giving_callback(self)
                low, high = self.chips
                self.chips.clear()
                self.low_goes_to.add_chip(low)
                self.high_goes_to.add_chip(high)

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        # parse the input
        self.factory_floor: Dict[str, Solver._ChipPassingProtocol] = {}
        self.log: Dict[str, Tuple[int, int]] = {}
        self.setup: List[Tuple[str, int]] = []

        def find(identifier: str) -> Solver._ChipPassingProtocol:
            if identifier not in self.factory_floor:
                if identifier.startswith("bot"):
                    self.factory_floor[identifier] = Solver._Robot(
                        identifier, self.callback
                    )
                if identifier.startswith("output"):
                    self.factory_floor[identifier] = Solver._OutputBin(identifier)
            return self.factory_floor[identifier]

        parse_lines(
            puzzle_input,
            (
                r"(?P<id>bot \d+) gives low to (?P<low_id>(?:bot|output) \d+) "
                r"and high to (?P<high_id>(?:bot|output) \d+)",
                lambda m: cast(Solver._Robot, find(m["id"])).instruction(
                    find(m["low_id"]),
                    find(m["high_id"]),
                ),
            ),
            (
                r"value (?P<value>\d+) goes to (?P<id>bot \d+)",
                lambda m: self.setup.append((m["id"], int(m["value"]))),
            ),
        )

        self.not_yet_run = True

    def callback(self, obj: _Robot) -> None:
        """Callback for when robots pass on values.

        Args:
            obj (_Robot): the Robot
        """
        if obj.chips == [17, 61]:
            self.part_one = int(str(obj).strip("bot "))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return self.part_one

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return prod([self.factory_floor[f"output {i}"].chips[0] for i in range(3)])

    def _run(self) -> None:
        """Setup the factory floor, and start the automonous robots."""
        if self.not_yet_run:
            for robot, value in self.setup:
                self.factory_floor[robot].add_chip(value)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
