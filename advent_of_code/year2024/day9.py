"""Solves the puzzle for Day 9 of Advent of Code 2024.

Disk Fragmenter

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/9
"""

from collections import deque
from copy import deepcopy
from dataclasses import dataclass

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 9
    TITLE = "Disk Fragmenter"

    @dataclass
    class _Block:
        position: int
        id: int
        size: int
        free: bool

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        disk_map = parse_tokens_single_line(puzzle_input, (r"\d", int_processor))
        self.input = []
        position = 0
        for i, size in enumerate(disk_map):
            self.input.append(Solver._Block(position, i // 2, size, i % 2 != 0))
            position += size

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        checksum = 0
        disk = deque(deepcopy(self.input))
        while disk:
            if disk[-1].size == 0 or disk[-1].free:
                disk.pop()
            elif disk[0].size == 0:
                disk.popleft()
            elif disk[0].free:
                checksum += disk[0].position * disk[-1].id
                disk[-1].size -= 1
                disk[0].size -= 1
                disk[0].position += 1
            else:
                checksum += disk[0].position * disk[0].id
                disk[0].size -= 1
                disk[0].position += 1
        return checksum

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        file_blocks = deepcopy(self.input[::2])
        free_blocks = deepcopy(self.input[1::2])

        for i, file in enumerate(reversed(file_blocks)):
            for free in free_blocks[: len(free_blocks) - i]:
                if file.size <= free.size:
                    file.position = free.position
                    free.size -= file.size
                    free.position += file.size
                    break

        return sum(
            (file.position + i) * file.id
            for file in file_blocks
            for i in range(file.size)
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
