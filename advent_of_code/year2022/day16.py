"""Solves the puzzle for Day 16 of Advent of Code 2022.

Proboscidea Volcanium

For puzzle specification and desciption, visit
https://adventofcode.com/2022/day/16
"""
from operator import itemgetter
from pathlib import Path
from sys import maxsize, path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2022
    DAY = 16
    TITLE = "Proboscidea Volcanium"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        lines = parse_lines(
            puzzle_input,
            (
                r"Valve ([A-Z][A-Z]) has flow rate=(\d+); "
                r"tunnels? leads? to valves? ([A-Z, ]+)",
                str_tuple_processor,
            ),
        )
        self.rates = {value: int(rate) for value, rate, _ in lines}
        self.routes = {value: values.split(", ") for value, _, values in lines}
        self.ready_to_solve = False

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        if not self.ready_to_solve:
            self._get_ready_to_solve()

        # find the route with the highest flow rates
        self.paths.clear()
        return self._find_routes("AA", ["AA"], 0, 30)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        if not self.ready_to_solve:
            self._get_ready_to_solve()

        self.paths.clear()
        self._find_routes("AA", ["AA"], 0, 26)
        del self.paths[("AA",)]

        # iterate over routes, keeping the max score for each set of values
        valve_sets: dict[frozenset[str], int] = {}
        for route, score in self.paths.items():
            frozen = frozenset(route[1:])
            valve_sets[frozen] = max(valve_sets.get(frozen, 0), score)

        # find the max score for two disjoint sets of values
        return max(
            human_score + elephant_score
            for human, human_score in valve_sets.items()
            for elephant, elephant_score in valve_sets.items()
            if human.isdisjoint(elephant)
        )

    def _get_ready_to_solve(self) -> None:
        """Prepare to solve."""
        # find all the useful nodes (ie positive flow rates)
        self.nodes = {"AA"} | {node for node, rate in self.rates.items() if rate > 0}

        # find distances betwen the useful nodes
        self.distances = {
            node: {
                dest: dist
                for dest, dist in self._dykstra_single_source_all_distances(
                    node
                ).items()
                if dest in self.nodes and dist
            }
            for node in self.nodes
        }

        self.paths: dict[tuple[str, ...], int] = {}

    def _dykstra_single_source_all_distances(self, initial: str) -> dict[str, int]:
        """Use Dykstra's Algorithm to find distances between source and all other nodes.

        Args:
            initial (str): the starting node

        Returns:
            dict[str, int]: dictionary of distances between nodes
        """
        routes = {
            start: {finish: 1 for finish in paths}
            for start, paths in self.routes.items()
        }

        distances = {node: maxsize for node in self.routes}
        distances[initial] = 0
        previous: dict[str, str] = {}
        visited: set[str] = set()

        while len(visited) < len(distances):
            current, dist = min(
                ((n, d) for n, d in distances.items() if n not in visited),
                key=itemgetter(1),
            )
            for neighbour, distance_to_neighbour in routes[current].items():
                tentative_distance = dist + distance_to_neighbour
                if (
                    neighbour not in visited
                    and tentative_distance < distances[neighbour]
                ):
                    distances[neighbour] = tentative_distance
                    previous[neighbour] = current
            visited.add(current)

        return distances

    def _find_routes(
        self, current: str, route: list[str], score: int, time: int
    ) -> int:
        """Recursively find all the routes between each valve.

        Args:
            current (str): the current valve
            route (list[str]): the route so far
            score (int): the current score
            time (int): the time remaining

        Returns:
            int: the best result from this branch
        """
        # turn on the value, and update the score
        if self.rates[current]:
            time -= 1
            score += self.rates[current] * time

        # record the paths (needed for part two)
        self.paths[tuple(route)] = score

        # calulate the next steps
        next_steps = [
            node
            for node, dist in self.distances[current].items()
            if (time - dist - 1) > 0 and node not in route
        ]

        # explore the next steps, if possible
        if next_steps:
            return max(
                self._find_routes(
                    next_step,
                    [*route, next_step],
                    score,
                    time - self.distances[current][next_step],
                )
                for next_step in next_steps
            )
        self.paths[tuple(route)] = score
        return score


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
