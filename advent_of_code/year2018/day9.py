"""Solves the puzzle for Day 9 of Advent of Code 2018.

Marble Mania

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/9
"""
from collections import defaultdict, deque
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_tuple_processor, parse_single_line
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 9
    TITLE = "Marble Mania"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.players, self.last = parse_single_line(
            puzzle_input,
            r"(\d+) players; last marble is worth (\d+) points",
            int_tuple_processor,
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(self.players, self.last)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(self.players, self.last * 100)

    def _solve(self, number_of_players: int, last_marble: int) -> int:
        """Solve the puzzle.

        Args:
            number_of_players (int): how many players are playing
            last_marble (int): what will be the last marble played

        Returns:
            int: the result
        """
        # use a double ended queue as the circle, with the right
        # hand element being the current marble
        marbles = deque([0])

        scores: defaultdict[int, int] = defaultdict(int)
        current_player = 1

        for i in range(1, last_marble + 1):
            if i % 23 != 0:
                marbles.rotate(-1)
                marbles.append(i)
            else:
                marbles.rotate(7)
                scores[current_player] += marbles.pop() + i
                marbles.rotate(-1)

            current_player = (current_player + 1) % number_of_players

        return max(scores.values())


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
