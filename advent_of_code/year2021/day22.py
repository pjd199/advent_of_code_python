"""Solves the puzzle for Day 22 of Advent of Code 2021.

Reactor Reboot

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/22
"""
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 22
    TITLE = "Reactor Reboot"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input: list[tuple[int, ...]] = [
            (
                1 if toggle == "on" else -1,
                int(min_x),
                int(max_x),
                int(min_y),
                int(max_y),
                int(min_z),
                int(max_z),
            )
            for toggle, min_x, max_x, min_y, max_y, min_z, max_z in parse_lines(
                puzzle_input,
                (
                    r"(on|off) "
                    r"x=(-?\d+)\.\.(-?\d+),"
                    r"y=(-?\d+)\.\.(-?\d+),"
                    r"z=(-?\d+)\.\.(-?\d+)",
                    str_tuple_processor,
                ),
            )
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(full_reboot=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(full_reboot=True)

    def _solve(self, full_reboot: bool) -> int:
        """Solve the puzzle.

        Args:
            full_reboot (bool): If true, fully reboot the reactor.

        Returns:
            int: the number of cubes turned on at the end
        """
        # select the steps to process
        steps = (
            self.input
            if full_reboot
            else [cube for cube in self.input if all(-50 <= x <= 50 for x in cube)]
        )

        # repeatedly add the steps to the reactor, everytime checking for any
        # intersections to add or remove
        reactor: list[tuple[int, ...]] = []
        for step in steps:
            updates = [step] if step[0] == 1 else []
            for cuboid in reactor:
                cube = (
                    -1 if cuboid[0] == 1 else 1,  # remove interesction for additions
                    step[1] if step[1] > cuboid[1] else cuboid[1],  # max
                    step[2] if step[2] < cuboid[2] else cuboid[2],  # min
                    step[3] if step[3] > cuboid[3] else cuboid[3],  # max
                    step[4] if step[4] < cuboid[4] else cuboid[4],  # min
                    step[5] if step[5] > cuboid[5] else cuboid[5],  # max
                    step[6] if step[6] < cuboid[6] else cuboid[6],  # min
                )
                if cube[1] <= cube[2] and cube[3] <= cube[4] and cube[5] <= cube[6]:
                    updates.append(cube)
            reactor.extend(updates)

        # sum the cuboids in the reactor
        return sum(
            magnitude * (max_x - min_x + 1) * (max_y - min_y + 1) * (max_z - min_z + 1)
            for magnitude, min_x, max_x, min_y, max_y, min_z, max_z in reactor
        )


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
