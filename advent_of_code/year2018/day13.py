"""Solves the puzzle for Day 13 of Advent of Code 2018.

Mine Cart Madness

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/13
"""
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from sys import path
from typing import Callable, Deque, Dict, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@dataclass
class Cart:
    """A Cart in the mine."""

    x: int
    y: int
    direction: str
    turn: int


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 13
    TITLE = "Mine Cart Madness"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.input = parse_lines(puzzle_input, (r"[\|\-/\\\+<>^v ]+", str_processor))

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        result, _ = self._solve()

        return result

    def solve_part_two(self) -> str:
        """Solve part two of the puzzle.

        Returns:
            str: the answer
        """
        _, result = self._solve()
        return result

    def _solve(self) -> Tuple[str, str]:
        """Solve the puzzle.

        Returns:
            Tuple[str,str]: the answer (part one, part two)
        """
        first_crash_location = ""

        # find the carts
        carts = [
            Cart(x, y, v, 0)
            for y, row in enumerate(self.input)
            for x, v in enumerate(row)
            if v in "<>^v"
        ]

        # create a track without the carts
        track_map = {c: c for c in "-+|/\\ "}
        track_map.update({"^": "|", "v": "|", ">": "-", "<": "-"})
        tracks = [[track_map[v] for v in row] for row in self.input]

        # create the mappings to progress state on each tick
        corner_moves = {
            (str("/"), str("^")): ">",
            (str("/"), str(">")): "^",
            (str("/"), str("v")): "<",
            (str("/"), str("<")): "v",
            (str("\\"), str("^")): "<",
            (str("\\"), str(">")): "v",
            (str("\\"), str("v")): ">",
            (str("\\"), str("<")): "^",
        }
        move_coordinates: Dict[str, Callable[[int, int], Tuple[int, int]]] = {
            "^": lambda x, y: (x, y - 1),
            ">": lambda x, y: (x + 1, y),
            "v": lambda x, y: (x, y + 1),
            "<": lambda x, y: (x - 1, y),
        }
        directions = "^>v<"

        # move all the carts, using a queue to manage the order in a single tick
        queue: Deque[Cart] = deque()
        while len(carts) > 1 or queue:
            if not queue:
                # get carts in order for next round
                queue.extend(sorted(carts, key=lambda c: (c.y, c.x)))

            # get the next cart to move
            cart = queue.popleft()

            # change direction if required
            track = tracks[cart.y][cart.x]
            if track == "+":
                # intersection
                cart.direction = directions[
                    (directions.index(cart.direction) + cart.turn - 1) % len(directions)
                ]
                cart.turn = (cart.turn + 1) % 3
            elif track in "\\/":
                # corner
                cart.direction = corner_moves[(track, cart.direction)]

            # move the cart
            cart.x, cart.y = move_coordinates[cart.direction](cart.x, cart.y)

            # check for a crash, where multiple carts are at the same location
            carts_at_same_location = [
                c for c in carts if c.x == cart.x and c.y == cart.y
            ]
            if len(carts_at_same_location) > 1:
                if not first_crash_location:
                    # store the location of the first crash
                    first_crash_location = f"{cart.x},{cart.y}"

                for c in carts_at_same_location:
                    # remove crashed carts and keep going
                    carts.remove(c)
                    if c in queue:
                        queue.remove(c)

        return first_crash_location, f"{carts[0].x},{carts[0].y}"


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
