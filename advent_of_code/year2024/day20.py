"""Solves the puzzle for Day 20 of Advent of Code 2024.

Race Condition

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/20
"""

from advent_of_code.utils.parser import parse_grid, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 20
    TITLE = "Race Condition"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        self.input = parse_grid(puzzle_input, r"[\.#SE]", str_processor)

    def _solve(self, limit: int) -> int:
        """Solve the puzzle.

        Args:
            limit (int): cheat time limit

        Returns:
            int: the result
        """
        markers = {val: (x, y) for (x, y), val in self.input.items()}

        # extract the path
        x, y = markers["S"]
        path = {(x, y): 0}
        distance = 0
        while (x, y) != markers["E"]:
            x, y = next(
                move
                for move in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
                if self.input[move] != "#" and move not in path
            )
            distance += 1
            path[(x, y)] = distance

        # count the cheats
        total = 0
        for x, y in path:
            cheats = (
                ((x + dx, y + dy), abs(dx) + abs(dy))
                for dx in range(-limit, limit + 1)
                for dy in range(-limit + abs(dx), limit + 1 - abs(dx))
                if (x + dx, y + dy) in path
            )
            for cheat, cost in cheats:
                if path[cheat] > path[(x, y)] + cost:
                    saving = path[cheat] - path[(x, y)] - cost
                    if saving >= 100:
                        total += 1
        return total

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(2)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(20)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
