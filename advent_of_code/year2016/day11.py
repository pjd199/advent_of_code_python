"""Solves the puzzle for Day 11 of Advent of Code 2016."""
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from itertools import combinations
from re import compile
from typing import DefaultDict, Deque, Iterable, List, Tuple

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
    def safe(self, others: List["Item"]) -> bool:
        """Determines if this is safe to store with other Items.

        Args:
            others (List[Item]): The other items

        Returns:
            bool: True if safe, otherwise False
        """


class Generator(Item):
    """The generator item."""

    def safe(self, others: List[Item]) -> bool:
        """Determines if this is safe to store with other Items.

        Args:
            others (List[Item]): The other items

        Returns:
            bool: True if safe, otherwise False
        """
        return True

    def __repr__(self) -> str:
        """The string representation of this object.

        Returns:
            str: The string representation of this object.
        """
        return f"{self.material} generator"


class Microchip(Item):
    """A Microchip item."""

    def safe(self, others: List[Item]) -> bool:
        """Determines if this is safe to store with other Items.

        Args:
            others (List[Item]): The other items

        Returns:
            bool: True if safe, otherwise False
        """
        return any(
            [isinstance(x, Generator) and self.material == x.material for x in others]
        ) or all([isinstance(x, Microchip) for x in others])

    def __repr__(self) -> str:
        """The string representation of this object.

        Returns:
            str: The string representation of this object.
        """
        return f"{self.material}-compatible microchip"


class State(ABC):
    """Represents a complete state in the simulation."""

    def __init__(self, elevator: int, floors: List[List[Item]], step: int) -> None:
        """Initialise the state.

        Args:
            elevator (int): the location of the elevator
            floors (List[List[Item]]): the floors in the state
            step (int): the number of steps away from the start
        """
        self.elevator = elevator
        self.floors = floors
        self.step = step

    def next_state(self) -> Iterable["State"]:
        """Iterator for all the safe moves from here.

        Yields:
            _type_: the next safe state
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

    def equivalence(self) -> Tuple[int, Tuple[Tuple[int, ...], ...]]:
        """Create a comparator of states, focusing on pairs rather than names.

        Returns:
            Tuple[int, Tuple[Tuple[int, int]]]: the formatted output
        """
        mapper: DefaultDict[str, List[int]] = defaultdict(lambda: [0, 0])
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

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) != 4
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        floor_number = {"first": 0, "second": 1, "third": 2, "fourth": 3}
        item_initializers = {"generator": Generator, "microchip": Microchip}

        floor_pattern = compile(
            rf"The (?P<floor_name>({'|'.join(floor_number.keys())})) floor contains "
            rf"(((a|and a) \w+(-compatible)? "
            rf"({'|'.join(item_initializers.keys())})[,. ]?)+"
            r"|nothing relevant.)"
        )
        item_pattern = compile(
            rf"(?P<material>\w+)(?:-compatible)? "
            rf"(?P<what>{'|'.join(item_initializers.keys())})"
        )
        # parse the input
        floors: List[List[Item]] = [[] for _ in range(len(floor_number))]
        for i, line in enumerate(puzzle_input):
            if m := floor_pattern.match(line):
                floor = floors[floor_number[m["floor_name"]]]
                for material, what in item_pattern.findall(line):
                    floor.append(item_initializers[what](material))
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

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
            Generator("elerium"),
            Microchip("elerium"),
            Generator("dilithium"),
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
        queue: Deque[State] = deque()
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
