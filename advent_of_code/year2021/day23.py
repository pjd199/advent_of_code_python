"""Solves the puzzle for Day 23 of Advent of Code 2021.

Amphipod

For puzzle specification and desciption, visit
https://adventofcode.com/2021/day/23
"""
from collections.abc import Generator
from heapq import heapify, heappop, heappush
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface

State = tuple[str, ...]


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2021
    DAY = 23
    TITLE = "Amphipod"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input_part_one = parse_grid(puzzle_input, r"[#. ABCD]", str_processor)
        self.input_part_two = parse_grid(
            puzzle_input[:3] + ["  #D#C#B#A#"] + ["  #D#B#A#C#"] + puzzle_input[3:],
            r"[#. ABCD]",
            str_processor,
        )
        self.room_map = {"A": 2, "B": 4, "C": 6, "D": 8}
        self.room_indices = set(self.room_map.values())
        self.move_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(self.input_part_one)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(self.input_part_two)

    def amphipods_can_leave(self, state: State, room: str) -> bool:
        """Determine if any amphipod can leave the room.

        Args:
            state (State): the state
            room (str): the room to check

        Returns:
            bool: True if any can leave, else false
        """
        return any(x != room for x in state[self.room_map[room]])

    def amphipods_can_enter(self, state: State, room: str) -> bool:
        """Determine if any amphipod can enter the room.

        Args:
            state (State): the state
            room (str): the room to check

        Returns:
            bool: True if any can enter, else false
        """
        return all(x == room for x in state[self.room_map[room]])

    def route_is_clear(self, state: State, a: int, b: int) -> bool:
        """Determine if the route betwen a and b is clear to travel.

        Args:
            state (State): the state
            a (int): point a
            b (int): point b

        Returns:
            bool: True is route a to b is clear to travel, otherwise False
        """
        return all(
            state[i] == "."
            for i in range(min(a, b) + 1, max(a, b))
            if i not in self.room_indices
        )

    def reachable_in_coridoor(
        self, state: State, start: int
    ) -> Generator[int, None, None]:
        """Iterate all the reachable spaces in the coridoor.

        Args:
            state (State): the state
            start (int): the starting index

        Yields:
            Generator[int, None, None]: Iterator of reachable spaces
        """
        for i in range(start, -1, -1):
            if i not in self.room_indices:
                if state[i] == ".":
                    yield i
                else:
                    break
        for i in range(start, len(state)):
            if i not in self.room_indices:
                if state[i] == ".":
                    yield i
                else:
                    break

    def _room_to_room(self, state: State) -> list[tuple[State, int]]:
        # If we can move an item straight from one room to another,
        # this is the best possible next move
        result = []
        for src_room, src_index in self.room_map.items():
            if self.amphipods_can_leave(state, src_room):
                item = state[src_index][0]
                dest_index = self.room_map[item]
                if self.amphipods_can_enter(state, item) and self.route_is_clear(
                    state, src_index, dest_index
                ):
                    # item able to leave and to enter it's destination
                    # and move to another room.
                    cost = (
                        (self.room_size - len(state[src_index]) + 1)  # up
                        + abs(dest_index - src_index)  # across
                        + (self.room_size - len(state[dest_index]))  # down
                    ) * self.move_costs[item]
                    next_state = list(state)
                    next_state[src_index] = state[src_index][1:]
                    next_state[dest_index] = item + state[dest_index]
                    result.append((tuple(next_state), cost))
        return result

    def _coridoor_to_room(self, state: State) -> list[tuple[State, int]]:
        # If we can move an from the coridoor into a room, then this
        # is the second best possible next move.
        result = []
        for src_index, item in enumerate(state):
            if src_index not in self.room_indices and item in "ABCD":
                dest_index = self.room_map[item]
                if self.amphipods_can_enter(state, item) and self.route_is_clear(
                    state, src_index, dest_index
                ):
                    # move the item from the coridoor into the room
                    cost = (
                        abs(dest_index - src_index)  # across
                        + (self.room_size - len(state[dest_index]))  # down
                    ) * self.move_costs[item]
                    next_state = list(state)
                    next_state[src_index] = "."
                    next_state[dest_index] = item + state[dest_index]
                    result.append((tuple(next_state), cost))
        return result

    def _other_moves(self, state: State) -> list[tuple[State, int]]:
        # If no other better move, yield the possible moves of items into
        # each different positions in the coridoor
        result = []
        for src_room, src_index in self.room_map.items():
            if self.amphipods_can_leave(state, src_room):
                item = state[src_index][0]
                for dest_index in self.reachable_in_coridoor(state, src_index):
                    cost = (
                        (self.room_size - len(state[src_index]) + 1)  # up
                        + abs(dest_index - src_index)  # across
                    ) * self.move_costs[item]
                    next_state = list(state)
                    next_state[src_index] = state[src_index][1:]
                    next_state[dest_index] = item
                    result.append((tuple(next_state), cost))

        return result

    def _next_state(self, state: State) -> list[tuple[State, int]]:
        """Iterate over possible next spaces.

        Args:
            state (State): the initial state

        Returns:
            list[tuple[State, int]]: Iterator of states
        """
        if result := self._room_to_room(state):
            return result

        if result := self._coridoor_to_room(state):
            return result

        return self._other_moves(state)

    def _solve(self, input_grid: dict[tuple[int, int], str]) -> int:
        # create the inital state
        max_y = max(y for _, y in input_grid)
        state: State = (
            ".",
            ".",
            "".join([input_grid[(3, y)] for y in range(2, max_y)]),
            ".",
            "".join([input_grid[(5, y)] for y in range(2, max_y)]),
            ".",
            "".join([input_grid[(7, y)] for y in range(2, max_y)]),
            ".",
            "".join([input_grid[(9, y)] for y in range(2, max_y)]),
            ".",
            ".",
        )
        self.room_size = len(state[2])

        # run Dykstra's algorithm until we reach the final state
        queue: list[tuple[int, State]] = [(0, state)]
        heapify(queue)
        costs: dict[State, int] = {state: 0}
        result = -1

        while queue:
            cost, state = heappop(queue)
            if cost > costs[state]:
                continue

            # check for final state - all rooms full and items have moved
            if (
                all(len(state[i]) == self.room_size for i in self.room_indices)
                and cost > 0
            ):
                result = cost
                break

            # explore the next state
            for next_state, additional_cost in self._next_state(state):
                tentative_cost = cost + additional_cost
                if next_state not in costs or tentative_cost < costs[next_state]:
                    costs[next_state] = tentative_cost
                    heappush(queue, (tentative_cost, next_state))

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
