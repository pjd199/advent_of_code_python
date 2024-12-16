"""Solves the puzzle for Day 12 of Advent of Code 2024.

Garden Groups

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/12
"""

from collections import deque
from collections.abc import Iterator, Sequence
from itertools import groupby

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 12
    TITLE = "Garden Groups"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[A-Z]+", str_processor)

    def _regions(self) -> Iterator[set[tuple[int, int]]]:
        """Iterator over the regions of the input.

        Yield:
            Iterator[set[tuple[int, int]]]: Iterator of the regions
        """
        grid = dict(self.input)
        while grid:
            (x, y), symbol = grid.popitem()

            # use a depth first search to find all the squares in the region
            queue = deque([(x, y)])
            visited = {(x, y)}
            while queue:
                x, y = queue.popleft()

                moves = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
                for move in moves:
                    if move in grid and grid[move] == symbol:
                        grid.pop(move)
                        visited.add(move)
                        queue.append(move)
            yield visited

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return sum(
            len(region)
            * sum(
                len({(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)} - region)
                for x, y in region
            )
            for region in self._regions()
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """

        def adjacent(x: int, y: int) -> Sequence[tuple[int, int]]:
            return [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]

        price = 0
        for region in self._regions():
            # find all the edge vectors of the region, working clockwise
            vectors = {
                vector
                for x, y in region
                for adjacent, vector in [
                    ((x + 1, y), ((x + 1, y), (x + 1, y + 1))),
                    ((x, y + 1), ((x + 1, y + 1), (x, y + 1))),
                    ((x - 1, y), ((x, y + 1), (x, y))),
                    ((x, y - 1), ((x, y), (x + 1, y))),
                ]
                if adjacent not in region
            }

            # trace the paths around the region
            while vectors:
                # pop any point on the path
                ((x, y), move) = vectors.pop()
                start = (x, y)
                # find the direction of travel for the vector
                direction = adjacent(x, y).index(move)
                path = deque([direction])
                x, y = move
                while (x, y) != start:
                    moves = adjacent(x, y)
                    if sum(1 for move in moves if ((x, y), move) in vectors) > 1:
                        direction = (direction + 1) % 4
                    move = moves[direction]
                    if ((x, y), move) in vectors:
                        vectors.remove(((x, y), move))
                        path.append(direction)
                        x, y = move
                    else:
                        direction = (direction + 1) % 4

                # sort out possible splits on first side
                while path[0] == path[-1]:
                    path.rotate()

                # caclulate the price
                price += len(region) * sum(1 for _ in groupby(path))

        return price


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
