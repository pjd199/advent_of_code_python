"""Solves the puzzle for Day 16 of Advent of Code 2021.

Packet Decoder

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/16
"""
from dataclasses import dataclass
from itertools import chain
from math import prod
from pathlib import Path
from sys import path
from typing import Callable

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_single_line, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Packet:
    """Represents a packet from the input."""

    version: int
    type_id: int
    value: int
    children: list["Packet"]


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 16
    TITLE = "Packet Decoder"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_single_line(puzzle_input, r"[0-9A-F]+", str_processor)
        self.ready = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self._decode_input()

        def sum_version(packet: Packet) -> int:
            return packet.version + sum(sum_version(p) for p in packet.children)

        return sum_version(self.root_packet)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._decode_input()

        def calc(packet: Packet) -> int:
            if packet.type_id == 4:
                return packet.value
            else:
                operator: dict[int, Callable[[list[int]], int]] = {
                    0: sum,
                    1: prod,
                    2: min,
                    3: max,
                    5: lambda x: 1 if x[0] > x[1] else 0,
                    6: lambda x: 1 if x[0] < x[1] else 0,
                    7: lambda x: 1 if x[0] == x[1] else 0,
                }
                return operator[packet.type_id]([calc(c) for c in packet.children])

        return calc(self.root_packet)

    def _decode_input(self) -> None:
        """Decode the input data."""
        if self.ready:
            return

        def decode(data: list[str]) -> tuple[Packet, list[str]]:
            version, data = int("".join(data[:3]), 2), data[3:]
            type_id, data = int("".join(data[:3]), 2), data[3:]
            if type_id == 4:
                content = []
                more = True
                while more:
                    more, value, data = (
                        (data[0] == "1"),
                        data[1:5],
                        data[5:],
                    )
                    content += value
                return Packet(version, type_id, int("".join(content), 2), []), data
            else:
                length_type_id, data = int(data[0], 2), data[1:]
                if length_type_id == 0:
                    length, data = int("".join(data[:15]), 2), data[15:]
                    children = []
                    end_length = len(data) - length
                    while len(data) > end_length:
                        child, data = decode(data)
                        children.append(child)
                    return Packet(version, type_id, 0, children), data
                else:
                    count, data = int("".join(data[:11]), 2), data[11:]
                    children = []
                    for _ in range(count):
                        child, data = decode(data)
                        children.append(child)
                    return Packet(version, type_id, 0, children), data

        self.root_packet, _ = decode(
            list(chain.from_iterable(f"{int(x,16):04b}" for x in self.input))
        )
        self.ready = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
