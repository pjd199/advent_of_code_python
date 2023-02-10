"""Solves the puzzle for Day 7 of Advent of Code 2019.

Amplification Circuit

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/7
"""
from itertools import permutations
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.IntcodeComputer import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 7
    TITLE = "Amplification Circuit"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.amplifiers = [IntcodeComputer(puzzle_input) for _ in range(5)]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(0, 4, feedback_loop=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(5, 9, feedback_loop=True)

    def _solve(self, min_phase: int, max_phase: int, feedback_loop: bool) -> int:
        """Solve the puzzle.

        Args:
            min_phase (int): the minimum phase setting
            max_phase (int): the maximum phase setting
            feedback_loop (bool): if True, enable the feedback loop

        Returns:
            int: _description_
        """
        result = -1
        for phase_settings in permutations(range(min_phase, max_phase + 1), 5):
            for amplifier, phase in zip(self.amplifiers, phase_settings):
                amplifier.reset()
                amplifier.append_input(phase)
            output = 0
            while not any(a.has_terminated() for a in self.amplifiers):
                for amplifier in self.amplifiers:
                    amplifier.append_input(output)
                    amplifier.execute(break_on_output=True)
                    if amplifier.has_terminated():
                        break
                    output = amplifier.read_output()
                if not feedback_loop:
                    break
            result = max(result, output)
        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
