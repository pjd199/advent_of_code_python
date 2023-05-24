"""Solves the puzzle for Day 23 of Advent of Code 2019.

Category Six

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/23
"""
from collections import deque
from copy import deepcopy
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 23
    TITLE = "Category Six"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        computer = IntcodeComputer(puzzle_input)
        self.computers = [deepcopy(computer) for _ in range(50)]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(exit_on_first_nat_value=True)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(exit_on_first_nat_value=False)

    def _solve(self, exit_on_first_nat_value: bool) -> int:
        # boot the computers
        for i, computer in enumerate(self.computers):
            computer.reset()
            computer.input_data(i, -1)

        # run the computers using a scheduler for computers when
        # they have input to read
        scheduler = deque(range(50))
        nat_x, nat_y = 0, 0
        nat_sent = deque([-1, -2], 2)

        while nat_sent[0] != nat_sent[1]:
            while scheduler:
                computer = self.computers[scheduler.popleft()]
                computer.execute(sleep_when_waiting_for_input=True)
                data = list(computer.iterate_output())
                while data:
                    address, x, y, *data = data
                    if address == 255:
                        nat_x, nat_y = x, y
                        if exit_on_first_nat_value:
                            return nat_y
                    else:
                        self.computers[address].input_data(x, y)
                        scheduler.append(address)
            self.computers[0].input_data(nat_x, nat_y)
            scheduler.append(0)
            nat_sent.append(nat_y)
        return nat_sent[-1]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
