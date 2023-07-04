"""Solves the puzzle for Day 20 of Advent of Code 2019.

Donut Maze

For puzzle specification and desciption, visit
https://adventofcode.com/2019/day/20
"""
from collections import deque
from heapq import heapify, heappop, heappush
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
    DAY = 20
    TITLE = "Donut Maze"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[ .#A-Z]", str_processor)
        self.routes: dict[str, list[tuple[str, int]]] = {}

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(multilevel=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(multilevel=True)

    def _prepare(self) -> None:
        if self.routes:
            return

        # identifiy the walkways and the walls
        self.walkway = {(x, y) for (x, y), v in self.input.items() if v == "."}
        self.walls = {(x, y) for (x, y), v in self.input.items() if v == "#"}

        # locate the portals
        letters = {(x, y): v for (x, y), v in self.input.items() if v.isupper()}
        portals = []
        for (x, y), v in letters.items():
            if (x, y - 1) in letters and (x, y + 1) in self.walkway:  # label above
                portals.append((letters[(x, y - 1)] + v, (x, y + 1)))
            elif (x, y + 1) in letters and (x, y - 1) in self.walkway:  # label below
                portals.append((v + letters[(x, y + 1)], (x, y - 1)))
            elif (x - 1, y) in letters and (x + 1, y) in self.walkway:  # label left
                portals.append((letters[(x - 1, y)] + v, (x + 1, y)))
            elif (x + 1, y) in letters and (x - 1, y) in self.walkway:  # label right
                portals.append((v + letters[(x + 1, y)], (x - 1, y)))

        # add the portals to the map, uniquely naming the pairs as we go
        self.portal_map: dict[str, tuple[int, int]] = {}
        for k, (x, y) in portals:
            k += "1" if (k + "0") in self.portal_map else "0"
            self.portal_map[k] = (x, y)

        self.portal_pairs = {
            k: (k[:2] + "0" if k[2] == "1" else k[:2] + "1")
            for k in self.portal_map
            if k not in ("AA0", "ZZ0")
        }

        # find the portals on the inside of the grid
        (min_x, max_x), (min_y, max_y) = ((min(a), max(a)) for a in zip(*self.walls))
        self.inner_portals = {
            k
            for k in self.portal_pairs
            if not (
                self.portal_map[k][0] in (min_x, max_x)
                or self.portal_map[k][1] in (min_y, max_y)
            )
        }

        # find the routes
        self._routes()

    def _routes(self) -> None:
        """Find the routes between each portal."""
        self.routes = {k: [] for k in self.portal_map}
        portal_locations = set(self.portal_map.values())
        self.portal_map_reversed = {v: k for k, v in self.portal_map.items()}
        for start, (start_x, start_y) in self.portal_map.items():
            # for each starting place, us a breadth first search to
            # find routes to the other portals
            queue: deque[tuple[tuple[int, int], int]] = deque([((start_x, start_y), 0)])
            visited = {(start_x, start_y)}
            while queue:
                (x, y), steps = queue.popleft()

                if (x, y) in portal_locations and (x, y) != (start_x, start_y):
                    # found a new route to add
                    self.routes[start].append((self.portal_map_reversed[(x, y)], steps))
                    continue

                moves = (
                    (x1, y1)
                    for x1, y1 in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
                    if (x1, y1) in self.walkway
                )
                for move in moves:
                    if move not in visited:
                        visited.add(move)
                        queue.append((move, steps + 1))

    def _solve(self, multilevel: bool) -> int:
        """Solve the puzzle.

        Args:
            multilevel (bool): when True, enable doughnut levels

        Returns:
            int: the shortest distance from AA to ZZ
        """
        self._prepare()

        # use Dysktra's Algorithm to explore the maze
        queue: list[tuple[int, str, int]] = [(0, "AA0", 0)]
        heapify(queue)
        distances: dict[tuple[str, int], int] = {("AA0", 0): 0}

        result = -1
        while queue:
            steps, node, level = heappop(queue)

            if level == 0 and node == "ZZ0":
                # we have reached the end!
                result = steps
                break

            for move, distance in self.routes[node]:
                tentative = steps + distance
                # check move distances within the current level
                if (move, level) not in distances or tentative < distances[
                    (move, level)
                ]:
                    distances[(move, level)] = tentative
                    heappush(queue, (tentative, move, level))

                # check move distances on another level
                if move not in ("AA0", "ZZ0") and (
                    level > 0 or move in self.inner_portals
                ):
                    other = self.portal_pairs[move]
                    tentative_other = tentative + 1
                    next_level = level
                    if multilevel:
                        next_level += 1 if move in self.inner_portals else -1
                    if (
                        (other, next_level) not in distances
                    ) or tentative_other < distances[(other, next_level)]:
                        distances[(other, next_level)] = tentative_other
                        heappush(queue, (tentative_other, other, next_level))

        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
