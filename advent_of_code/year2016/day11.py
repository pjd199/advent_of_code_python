"""Solves the puzzle for Day 11 of Advent of Code 2016.

Radioisotope Thermoelectric Generators

For puzzle specification and desciption, visit
https://adventofcode.com/2016/day/11
"""
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from collections.abc import Generator
from itertools import combinations
from pathlib import Path
from re import findall
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Item(ABC):
    """Class to represent an item on the floor."""

    def __init__(self, material: str) -> None:
        """Initialises the item.

        Args:
            material (str): The material of the item
        """
        self.material = material

    @abstractmethod
    def safe(self, others: list["Item"]) -> bool:
        """Determines if this is safe to store with other Items.

        Args:
            others (list[Item]): The other items

        Returns:
            bool: True if safe, otherwise False
        """


class Generator_Item(Item):
    """The generator item."""

    def safe(self, others: list[Item]) -> bool:
        """Determines if this is safe to store with other Items.

        Args:
            others (list[Item]): The other items

        Returns:
            bool: True if safe, otherwise False
        """
        return True

    def __repr__(self) -> str:
        """The string representation of this object.

        Returns:
            str: The string representation of this object.
        """
        return f"{self.material} generator"  # pragma: no cover


class Microchip(Item):
    """A Microchip item."""

    def safe(self, others: list[Item]) -> bool:
        """Determines if this is safe to store with other Items.

        Args:
            others (list[Item]): The other items

        Returns:
            bool: True if safe, otherwise False
        """
        return any(
            [
                isinstance(x, Generator_Item) and self.material == x.material
                for x in others
            ]
        ) or all([isinstance(x, Microchip) for x in others])

    def __repr__(self) -> str:
        """The string representation of this object.

        Returns:
            str: The string representation of this object.
        """
        return f"{self.material}-compatible microchip"  # pragma: no cover


class State(ABC):
    """Represents a complete state in the simulation."""

    def __init__(self, elevator: int, floors: list[list[Item]], step: int) -> None:
        """Initialise the state.

        Args:
            elevator (int): the location of the elevator
            floors (list[list[Item]]): the floors in the state
            step (int): the number of steps away from the start
        """
        self.elevator = elevator
        self.floors = floors
        self.step = step

    def next_state(self) -> Generator["State", None, None]:
        """Iterator for all the safe moves from here.

        Yields:
            Generator["State", None, None]: the next safe state
        """
        for items_in_elevator in [2, 1]:
            for items in combinations(self.floors[self.elevator], items_in_elevator):
                for move in [1, -1]:
                    new_elevator = self.elevator + move
                    if new_elevator in range(len(self.floors)):
                        # move the items to the new floor
                        new_floors = [
                            [x for x in floor if x not in items]
                            for floor in self.floors
                        ]
                        new_floors[new_elevator] += items

                        if all(
                            y.safe(new_floors[i])
                            for i, x in enumerate(new_floors)
                            for y in x
                        ):
                            yield State(new_elevator, new_floors, self.step + 1)

    def equivalence(self) -> tuple[int, tuple[tuple[int, ...], ...]]:
        """Create a comparator of states, focusing on pairs rather than names.

        Returns:
            tuple[int, tuple[tuple[int, ...], ...]]: the formatted output
        """
        mapper: defaultdict[str, list[int]] = defaultdict(lambda: [0, 0])
        for i, floor in enumerate(self.floors):
            for item in floor:
                if isinstance(item, Microchip):
                    mapper[item.material][0] = i
                else:
                    mapper[item.material][1] = i
        tuples = tuple(sorted([tuple(x) for x in mapper.values()]))
        return (self.elevator, tuples)


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 11
    TITLE = "Radioisotope Thermoelectric Generators"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        item_initializers = {"generator": Generator_Item, "microchip": Microchip}
        floors = parse_lines(
            puzzle_input,
            (
                r"The (first|second|third|fourth) floor contains "
                r"(?P<contents>((a|and a) \w+(-compatible)? "
                r"(generator|microchip)[,. ]*)+"
                r"|nothing relevant.)",
                lambda m: [
                    item_initializers[what](material)
                    for material, what in findall(
                        r"(?P<material>\w+)(?:-compatible)? "
                        r"(?P<what>generator|microchip)",
                        m["contents"],
                    )
                ],
            ),
        )

        self.start_state = State(0, floors, 0)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._run(self.start_state)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        floors = self.start_state.floors
        floors[0] += [
            Generator_Item("elerium"),
            Microchip("elerium"),
            Generator_Item("dilithium"),
            Microchip("dilithium"),
        ]

        return self._run(State(0, floors, 0))

    def _run(self, initial_state: State) -> int:
        """Run the simulation, using a Breadth First Search Algorithm.

        Args:
            initial_state (State): Initial state

        Returns:
            int: the number of steps required to move all items.
        """
        # setup the queue and the visited set
        queue: deque[State] = deque()
        queue.append(initial_state)
        visited = {initial_state.equivalence()}

        result = -1
        while queue and result == -1:
            state = queue.popleft()
            for next_state in state.next_state():
                if all(
                    len(next_state.floors[i]) == 0
                    for i in range(len(next_state.floors) - 1)
                ):
                    # all items on top floor
                    result = next_state.step
                    break

                equivalence = next_state.equivalence()
                if equivalence not in visited:
                    visited.add(equivalence)
                    queue.append(next_state)
        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
