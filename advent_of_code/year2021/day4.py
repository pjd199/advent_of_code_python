"""Solves the puzzle for Day 4 of Advent of Code 2021.

Giant Squid

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/4
"""
from pathlib import Path
from sys import path
from typing import List, Set

import numpy as np

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    int_processor,
    parse_tokens,
    parse_tokens_single_line,
    split_sections,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 4
    TITLE = "Giant Squid"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input)
        self.numbers = parse_tokens_single_line(
            sections[0], (r"\d+", int_processor), delimiter=","
        )
        self.boards = [
            parse_tokens(section, (r"\d+", int_processor), delimiter=" ")
            for section in sections[1:]
        ]
        self.winning_scores: List[int] = []

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._play_bingo()
        return self.winning_scores[0]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._play_bingo()
        return self.winning_scores[-1]

    def _play_bingo(self) -> None:
        if self.winning_scores:
            return

        boards = np.array([np.array(b) for b in self.boards])
        marks = np.full_like(boards, False, dtype=np.bool_)
        visited: Set[int] = set()

        for number in self.numbers:
            # mark the new number as seen
            marks[np.nonzero(boards == number)] = True

            # find the wining boards
            round_winners = np.any(
                np.logical_or(
                    np.all(marks, axis=2),
                    np.all(marks.transpose(0, 2, 1), axis=2),
                ),
                axis=1,
            )

            # record new winners
            completed = np.transpose(np.nonzero(round_winners))
            if len(completed) > len(visited):
                for x in completed:
                    board = x[0]
                    if board not in visited:
                        visited.add(board)
                        score = np.sum(boards[board], where=~marks[board]) * number
                        self.winning_scores.append(score)
                if len(self.winning_scores) == len(boards):
                    break


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
