"""Solves the puzzle for Day 25 of Advent of Code 2017.

The Halting Problem

For puzzle specification and desciption, visit
https://adventofcode.com/2017/day/25
"""
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from sys import path
from typing import DefaultDict, Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class _Action:
    value: int
    move: int
    next_state: str


@dataclass
class _State:
    actions: List[_Action] = field(default_factory=list)


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2017
    DAY = 25
    TITLE = "The Halting Problem"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        tokens = iter(
            parse_lines(
                puzzle_input,
                (r"Begin in state ([A-Z]).", lambda m: m[1]),
                (r"Perform a diagnostic checksum after (\d+) steps.", lambda m: m[1]),
                (r"In state ([A-Z]):", lambda m: m[1]),
                (r"  If the current value is ([01]):", lambda m: m[1]),
                (r"    - Write the value ([01]).", lambda m: m[1]),
                (
                    r"    - Move one slot to the (left|right).",
                    lambda m: -1 if m[1] == "left" else 1,
                ),
                (r"    - Continue with state ([A-Z]).", lambda m: m[1]),
                (r"", lambda m: "BLANK"),
                min_length=12,
            )
        )
        self.input: Dict[str, _State] = {}
        self.start_state = str(next(tokens))
        self.stop = int(next(tokens))
        while next(tokens, False):
            s = _State([])
            self.input[str(next(tokens))] = s
            for _ in range(2):
                next(tokens)
                s.actions.append(
                    _Action(int(next(tokens)), int(next(tokens)), str(next(tokens)))
                )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        tape: DefaultDict[int, int] = defaultdict(int)
        cursor = 0
        state = self.start_state

        # run the Turing Machine
        for _ in range(self.stop):
            action = self.input[state].actions[tape[cursor]]
            tape[cursor] = action.value
            cursor += action.move
            state = action.next_state

        return sum(tape.values())

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Raises:
            NotImplementedError: always!
        """
        raise NotImplementedError("No part two on Christmas Day!!!")

    def solve_all(self) -> List[int]:
        """Solve the one and only part to this puzzle.

        Returns:
            List[int]: the result
        """
        return [self.solve_part_one()]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
