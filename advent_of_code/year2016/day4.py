"""Solves the puzzle for Day 4 of Advent of Code 2016.

Security Through Obscurity

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/10
"""
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from string import ascii_lowercase
from sys import path
from typing import DefaultDict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import dataclass_processor, parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    @dataclass
    class _Room:
        encrypted_name: str
        sector_id: int
        checksum: str

    YEAR = 2016
    DAY = 4
    TITLE = "Security Through Obscurity"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(
            puzzle_input,
            (
                r"(?P<encrypted_name>[a-z\-]+)"
                r"(?P<sector_id>[0-9]+)"
                r"\[(?P<checksum>[a-z]{5})\]",
                dataclass_processor(Solver._Room),
            ),
        )
        self.real_rooms: List[Solver._Room] = []

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.real_rooms:
            self._find_real_rooms()

        return sum([x.sector_id for x in self.real_rooms])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.real_rooms:
            self._find_real_rooms()

        result = 0
        for room in self.real_rooms:
            decrypted = []
            for c in room.encrypted_name:
                if c == "-":
                    decrypted.append(" ")
                else:
                    decrypted.append(
                        ascii_lowercase[((ord(c) - ord("a")) + room.sector_id) % 26]
                    )
                if "".join(decrypted).strip() == "northpole object storage":
                    result = room.sector_id
                    break

        return result

    def _find_real_rooms(self) -> None:
        """Find the real rooms."""
        self.real_rooms = []
        for room in self.input:
            # count the frequency of letters
            counter: DefaultDict[str, int] = defaultdict(int)
            for c in room.encrypted_name:
                if c != "-":
                    counter[str(c)] += 1
            # order the list by freqency, then alphabetical
            ordered = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
            checksum = "".join([x[0] for x in ordered[:5]])
            if room.checksum == checksum:
                self.real_rooms.append(room)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
