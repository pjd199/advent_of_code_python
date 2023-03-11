"""Solves the puzzle for Day 17 of Advent of Code 2019.

Set and Forget

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/17
"""
from collections import deque
from itertools import islice
from pathlib import Path
from sys import path
from typing import Callable, Dict, Iterator, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 17
    TITLE = "Set and Forget"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        self.computer = IntcodeComputer(puzzle_input)
        self.grid: Dict[Tuple[int, int], str] = {}

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.read_grid()
        min_x, min_y = (min(a) for a in zip(*self.grid))
        points = {(x, y) for (x, y), v in self.grid.items() if v in "#^>v<"}
        intersections = {
            (x, y)
            for x, y in points
            if {(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)} < points
        }
        return sum(abs(x - min_x) * abs(y - min_y) for x, y in intersections)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        # calculate the list of commands Lx Rx
        self.read_grid()
        route = self.full_route() + ","

        # find substrings a,b,c
        a = b = c = ""
        for x in self.subs(route):
            route_minus_x = route.replace(x, "")
            for y in self.subs(route_minus_x):
                route_minus_xy = route_minus_x.replace(y, "")
                for z in self.subs(route_minus_xy.replace(y, "")):
                    if route_minus_xy.replace(z, "") == "":
                        a, b, c = x, y, z

        # find the main routine
        main = route.replace(a, "A,").replace(b, "B,").replace(c, "C,")

        # strip off the execess comma
        a, b, c, main = (x.strip(",") for x in (a, b, c, main))

        # send input to the computer, and read the result (final output number)
        self.computer.reset()
        self.computer.memory[0] = 2
        self.computer.input_data(*map(ord, f"{main}\n{a}\n{b}\n{c}\nn\n"))
        self.computer.execute()
        return deque(self.computer.iterate_output(), 1).pop()

    def read_grid(self) -> None:
        """Read the grid from the computer, but only once."""
        if self.grid:
            return

        self.computer.reset()
        self.computer.execute()
        self.grid = parse_grid(
            "".join(map(chr, self.computer.iterate_output())).strip().splitlines(),
            r"[.#^>v<]",
            str_processor,
        )

    def full_route(self) -> str:
        """Find the instruction string to follow the full route.

        Returns:
            str: the instruction string
        """
        # select the useful points and the starting values
        points = {(x, y) for (x, y), v in self.grid.items() if v in "#^>v<"}
        (x, y), arrow = next(
            ((x, y), v) for (x, y), v in self.grid.items() if v in "^>v<"
        )

        # prepare the navigate
        arrows = ["^", ">", "v", "<"]
        direction = arrows.index(arrow)
        looks: Dict[int, Callable[[int, int], Tuple[int, int]]] = {
            0: lambda x1, y1: (x1, y1 - 1),
            1: lambda x1, y1: (x1 + 1, y1),
            2: lambda x1, y1: (x1, y1 + 1),
            3: lambda x1, y1: (x1 - 1, y1),
        }
        route = []
        turn = ""
        move = 0

        # navigate the points, recording the instructions
        while True:
            if looks[direction](x, y) in points:
                move += 1
                x, y = looks[direction](x, y)
            else:
                if move:
                    route.extend([turn, str(move)])
                    move = 0
                if looks[(direction + 1) % len(looks)](x, y) in points:
                    direction = (direction + 1) % len(looks)
                    turn = "R"
                elif looks[(direction - 1) % len(looks)](x, y) in points:
                    direction = (direction - 1) % len(looks)
                    turn = "L"
                else:
                    break

        return ",".join(route)

    def subs(self, route: str) -> Iterator[str]:
        """Helper function, to find possible substrings.

        Args:
            route (str): the starting route

        Yields:
            Tuple[str]: the substrings
        """
        comma_locations = (i for i, v in enumerate(route[:20]) if v == ",")
        yield from (route[: i + 1] for i in islice(comma_locations, 1, None, 2))


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
