"""Solves the puzzle for Day 25 of Advent of Code 2019.

Cryostasis

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/25
"""
from collections import deque
from copy import deepcopy
from itertools import combinations
from pathlib import Path
from re import findall, search
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface
from advent_of_code.year2019.intcode import IntcodeComputer


class Robot(IntcodeComputer):
    """A subclass to accept string input."""

    def input_ascii(self, command: str) -> None:
        """Recieve a command for the robot.

        Args:
            command (str): the command
        """
        self.input_data(*[ord(x) for x in command])

    def read_ascii_until_input_required(self) -> str:
        """Read the output until a command input is required.

        Returns:
            str: the output
        """
        self.execute(sleep_when_waiting_for_input=True)
        return "".join([chr(x) for x in self.iterate_output()])


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 25
    TITLE = "Cryostasis"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.robot = Robot(puzzle_input)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        self.robot.reset()

        # explore the ship, finding routes and the items
        queue: deque[tuple[Robot, list[str]]] = deque([(deepcopy(self.robot), [])])
        visited = set()
        routes = {}
        locations = {}
        helpful_items = set()
        deadly_items = {
            "infinite loop",
            "giant electromagnet",
            "molten lava",
            "escape pod",
            "photons",
        }
        while queue:
            robot, path = queue.pop()
            response = robot.read_ascii_until_input_required()
            match = search(r"== ([A-Za-z ]+) ==", response)
            if match and match[1] not in visited:
                room = match[1]
                routes[room] = path
                visited.add(room)
                doors = findall(r"(north|south|east|west)", response)
                for door in doors:
                    next_robot = deepcopy(robot)
                    next_robot.input_ascii(f"{door}\n")
                    queue.append((next_robot, path + [door]))
                # find the items to pick collect
                match = search(r"Items here:\n(- .*\n)\n", response)
                if match:
                    for item in findall(r"- ([A-Za-z ]*)", match[1]):
                        if item not in helpful_items and item not in deadly_items:
                            helpful_items.add(item)
                            locations[item] = room

        # collect the items, then move to the security checkpoint
        robot = deepcopy(self.robot)
        back = {"north": "south", "south": "north", "east": "west", "west": "east"}
        commands = "".join(
            [
                (
                    "".join([f"{x}\n" for x in routes[locations[item]]])
                    + f"take {item}\n"
                    + "".join(
                        [f"{back[x]}\n" for x in reversed(routes[locations[item]])]
                    )
                )
                for item in helpful_items
            ]
        ) + "".join(f"{x}\n" for x in routes["Security Checkpoint"])
        robot.input_ascii(commands)
        response = robot.read_ascii_until_input_required()

        # find the right item weight combination for the security gate
        result = -1
        holding = tuple(helpful_items)
        for items in combinations(helpful_items, 4):  # always 4 items
            # take and drop items as needed
            commands = (
                "".join([f"drop {item}\n" for item in holding if item not in items])
                + "".join([f"take {item}\n" for item in items if item not in holding])
                + "west\n"
            )
            holding = items
            robot.input_ascii(commands)
            response = robot.read_ascii_until_input_required()
            # check the response for the airlock code
            if m := search(r"(\d+) on the keypad", response):
                result = int(m[1])
                break

        return result

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: but never does!

        Raises:
            NotImplementedError: always!
        """
        raise NotImplementedError("No part two on Christmas Day!!!")


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
