"""Solves the puzzle for Day 4 of Advent of Code 2016."""
from collections import defaultdict
from dataclasses import dataclass
from re import compile
from string import ascii_lowercase
from typing import List, Optional

from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    @dataclass
    class _Room:
        encrypted_name: str
        decrypted_name: Optional[str]
        sector_id: int
        checksum: str

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        self.input = []
        pattern = compile(r"(?P<name>[a-z\-]+)(?P<id>[0-9]+)\[(?P<checksum>[a-z]{5})\]")
        for i, line in enumerate(puzzle_input):
            if m := pattern.match(line):
                self.input.append(
                    Solver._Room(
                        encrypted_name=m["name"],
                        sector_id=int(m["id"]),
                        checksum=m["checksum"],
                        decrypted_name=None,
                    )
                )
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i}")

        self.real_rooms = []

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

    def _find_real_rooms(self):
        """Find the real rooms."""
        self.real_rooms = []
        for room in self.input:
            # count the frequency of letters
            counter = defaultdict(int)
            for c in room.encrypted_name:
                if c != "-":
                    counter[str(c)] += 1
            # order the list by freqency, then alphabetical
            ordered = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
            checksum = "".join([x[0] for x in ordered[:5]])
            if room.checksum == checksum:
                self.real_rooms.append(room)
