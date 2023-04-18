"""Solves the puzzle for Day 2 of Advent of Code 2019.

1202 Program Alarm

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/2
"""
from itertools import product
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))


from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 2
    TITLE = "1202 Program Alarm"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.computer = IntcodeComputer(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.computer.reset()
        self.computer.memory[1] = 12
        self.computer.memory[2] = 2
        self.computer.execute()
        return self.computer.memory[0]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        result = -1
        for noun, verb in product(range(100), range(100)):
            self.computer.reset()
            self.computer.memory[1] = noun
            self.computer.memory[2] = verb
            self.computer.execute()
            if self.computer.memory[0] == 19690720:
                result = (100 * noun) + verb
                break

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
