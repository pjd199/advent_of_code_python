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

from advent_of_code.utils.parser import parse_lines, split_sections, str_processor_group
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
        # split the sections for parsing
        sections = split_sections(puzzle_input)

        # parse the initial state and target
        self.start_state, stop = parse_lines(
            sections[0],
            (r"Begin in state ([A-Z]).", str_processor_group(1)),
            (
                r"Perform a diagnostic checksum after (\d+) steps.",
                str_processor_group(1),
            ),
            min_length=2,
            max_length=2,
        )
        self.stop = int(stop)

        # parse the state transitions
        self.input: Dict[str, _State] = {}
        for section in sections[1:]:
            tokens = parse_lines(
                section,
                (r"In state ([A-Z]):", str_processor_group(1)),
                (r"  If the current value is ([01]):", str_processor_group(1)),
                (r"    - Write the value ([01]).", str_processor_group(1)),
                (
                    r"    - Move one slot to the (left|right).",
                    str_processor_group(1),
                ),
                (r"    - Continue with state ([A-Z]).", str_processor_group(1)),
                min_length=9,
                max_length=9,
            )
            state = tokens[0]
            moves = [tokens[2:5], tokens[6:9]]

            self.input[state] = _State(
                [
                    _Action(int(move[0]), -1 if move[1] == "left" else 1, move[2])
                    for move in moves
                ]
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
