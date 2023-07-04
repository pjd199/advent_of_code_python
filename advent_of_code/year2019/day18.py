"""Solves the puzzle for Day 18 of Advent of Code 2019.

Many-Worlds Interpretation

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/18
"""
from collections import deque
from heapq import heapify, heappop, heappush
from itertools import chain
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2019
    DAY = 18
    TITLE = "Many-Worlds Interpretation"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[@.#A-Za-z]", str_processor)

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(self.input)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        x, y = next((x, y) for (x, y), v in self.input.items() if v == "@")
        return self._solve(
            self.input
            | {
                (x - 1, y - 1): "@",
                (x, y - 1): "#",
                (x + 1, y - 1): "@",
                (x - 1, y): "#",
                (x, y): "#",
                (x + 1, y): "#",
                (x - 1, y + 1): "@",
                (x, y + 1): "#",
                (x + 1, y + 1): "@",
            }
        )

    def _solve(self, grid: dict[tuple[int, int], str]) -> int:
        """Solve the puzzle, using Dysktra's Algorithm.

        Args:
            grid (dict[tuple[int, int], str]): the input grid to use

        Returns:
            int: the shortest path to collect all the keys in the grid
        """
        # a set of all the keys to find
        keys_to_find = {v: (x, y) for (x, y), v in self.input.items() if v.islower()}
        # place a robot at each of the starting locations
        starting_locations = {
            k: str(i) for i, k in enumerate(k for k, v in grid.items() if v == "@")
        }
        grid = grid | starting_locations
        robots = tuple(starting_locations.values())

        # find all the routes
        routes = {k: self._find_routes(k, grid) for k in chain(keys_to_find, robots)}

        # start Dykstra's algorithm with an initial state
        state: tuple[int, tuple[str, ...], frozenset[str]] = (
            0,
            robots,
            frozenset({}),
        )
        queue = [state]
        distances: dict[tuple[tuple[str, ...], frozenset[str]], int] = {
            (robots, frozenset()): 0
        }
        heapify(queue)

        result = -1
        while queue:
            # pop the next best state to explore
            distance, robots, keys_in_hand = heappop(queue)

            # terminate once all keys have been found
            if len(keys_in_hand) == len(keys_to_find):
                result = distance
                break

            # all all the possible next states to the queue
            for i, robot in enumerate(robots):
                for dest, (keys_required, additional_distance) in routes[robot].items():
                    if keys_required <= keys_in_hand:
                        # found a route we can unlock
                        tentative = distance + additional_distance
                        next_robots = list(robots)
                        next_robots[i] = dest
                        next_state = (
                            tuple(next_robots),
                            keys_in_hand | {dest},
                        )
                        if (
                            next_state not in distances
                            or tentative < distances[next_state]
                        ):
                            # found the best distance so far
                            distances[next_state] = tentative
                            heappush(queue, (tentative, *next_state))

        return result

    def _find_routes(
        self, start: str, grid: dict[tuple[int, int], str]
    ) -> dict[str, tuple[frozenset[str], int]]:
        """Find routes from the start key to the next key.

        Args:
            start (str): the start key
            grid (dict[tuple[int, int], str]): the grid to explore

        Returns:
            dict[str, tuple[frozenset[str], int]]: the results
        """
        start_location = next((x, y) for (x, y), v in grid.items() if v == start)

        # use a depth first search to explore the grid
        results: dict[str, tuple[frozenset[str], int]] = {}
        queue: deque[tuple[tuple[int, int], int, frozenset[str]]] = deque(
            [(start_location, 0, frozenset())]
        )
        visited = {start_location}

        while queue:
            # pop the next location off the queue
            (x, y), steps, keys_required = queue.popleft()

            # generate the next moves
            moves = (
                (m, grid[m])
                for m in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
                if grid[m] != "#" and m not in visited
            )

            for move, item in moves:
                visited.add(move)
                if item.isupper():
                    # found a door, so add it's key to keys_required
                    queue.append(
                        (move, steps + 1, frozenset(keys_required | {item.lower()}))
                    )
                elif item.islower():
                    # found a key
                    results[item] = (keys_required, steps + 1)
                else:
                    # add the next step to the queue
                    queue.append((move, steps + 1, keys_required))

        return results


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
