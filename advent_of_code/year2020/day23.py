"""Solves the puzzle for Day 23 of Advent of Code 2020.

Crab Cups

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/23
"""
from pathlib import Path
from sys import path
from typing import List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_tokens_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 23
    TITLE = "Crab Cups"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_tokens_single_line(puzzle_input, (r"\d", int_processor))

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        result = self._solve(number_of_cups=9, cycles=100)
        return "".join([str(x) for x in result])

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        result = self._solve(number_of_cups=1000000, cycles=10000000)
        return result[0] * result[1]

    def _solve(self, number_of_cups: int, cycles: int) -> List[int]:
        """Solve the puzzle.

        Args:
            number_of_cups (int): number of cups in play
            cycles (int): number of cycles to play

        Returns:
            List[int]: the final order, after cup 1
        """
        # create a list of cups in play
        cups = list(self.input)
        cups.extend(range(len(cups) + 1, number_of_cups + 1))
        current_cup = cups[0]

        # create a linked list in a array
        linked_list = [0] * (len(cups) + 1)
        for i in range(len(cups) - 1):
            linked_list[cups[i]] = cups[i + 1]
        linked_list[cups[-1]] = current_cup

        for _ in range(cycles):
            # get the next three cups, and remember what the next cup will be
            cup1 = linked_list[current_cup]
            cup2 = linked_list[cup1]
            cup3 = linked_list[cup2]
            next_cup = linked_list[cup3]

            # work out the destination
            dest = number_of_cups if current_cup == 1 else current_cup - 1
            while dest in [cup1, cup2, cup3]:
                dest = number_of_cups if dest == 1 else dest - 1

            # remove the three cups from the linked list
            # and place after the destination cup
            linked_list[current_cup] = linked_list[cup3]
            linked_list[cup3] = linked_list[dest]
            linked_list[dest] = cup1

            # move to the next cup
            current_cup = next_cup

        # put the linked list into readable order, following cup 1
        result: List[int] = []
        x = linked_list[1]
        while x != 1:
            result.append(x)
            x = linked_list[x]
        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
