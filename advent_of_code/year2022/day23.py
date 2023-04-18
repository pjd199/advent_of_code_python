"""Solves the puzzle for Day 23 of Advent of Code 2022.

Unstable Diffusion

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/23
"""
from collections import Counter, deque
from pathlib import Path
from sys import path
from typing import Callable, Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 23
    TITLE = "Unstable Diffusion"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[.#]", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(10)[0]

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(10000)[1]

    def _solve(self, rounds: int) -> Tuple[int, int]:
        elves = {k for k, v in self.input.items() if v == "#"}

        take_move: Dict[str, Callable[[int, int], Tuple[int, int]]] = {
            "N": lambda x, y: (x, y - 1),
            "S": lambda x, y: (x, y + 1),
            "W": lambda x, y: (x - 1, y),
            "E": lambda x, y: (x + 1, y),
        }

        order = deque(["N", "S", "W", "E"])

        last_round = -1
        for current_round in range(rounds):
            # propose the moves
            moves = {}
            for x, y in elves:
                look = {
                    "NW": (x - 1, y - 1) in elves,
                    "N": (x, y - 1) in elves,
                    "NE": (x + 1, y - 1) in elves,
                    "W": (x - 1, y) in elves,
                    "E": (x + 1, y) in elves,
                    "SW": (x - 1, y + 1) in elves,
                    "S": (x, y + 1) in elves,
                    "SE": (x + 1, y + 1) in elves,
                }
                if any(look.values()):
                    for direction in order:
                        if not any(v for k, v in look.items() if direction in k):
                            moves[(x, y)] = take_move[direction](x, y)
                            break

            # has anyone moved?
            if not moves:
                last_round = current_round
                break

            # move the elf only if no other elves want to move there
            counter = Counter(moves.values())
            unique_moves = {k: v for k, v in moves.items() if counter[v] == 1}
            elves.difference_update(unique_moves.keys())
            elves.update(unique_moves.values())

            # change the starting order
            order.rotate(-1)

        # finished the rounds, so calculate the area bounding box, then return
        (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*elves))
        area = ((max_x - min_x + 1) * (max_y - min_y + 1)) - len(elves)

        return area, last_round + 1


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
