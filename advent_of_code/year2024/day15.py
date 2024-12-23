"""Solves the puzzle for Day 15 of Advent of Code 2024.

Warehouse Woes

For puzzle specification and desciption, visit
https://adventofcode.com/2024/day/15
"""

from collections import deque
from itertools import pairwise

from advent_of_code.utils.parser import (
    parse_grid,
    parse_tokens_single_line,
    split_sections,
    str_processor,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2024
    DAY = 15
    TITLE = "Warehouse Woes"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        grid, moves = split_sections(puzzle_input, expected_sections=2)

        self.grid = parse_grid(grid, r"[#.O@]", str_processor)

        expand = {"#": "##", "O": "[]", ".": "..", "@": "@."}
        expanded_grid = ["".join(expand[char] for char in line) for line in grid]
        self.expanded_grid = parse_grid(expanded_grid, r"[#.\[\]@]", str_processor)

        self.moves = parse_tokens_single_line(
            ["".join(moves)], (r"[>v<^]", str_processor)
        )

    def _solve(self, grid: dict[tuple[int, int], str]) -> int:
        """Solve the puzzle.

        Args:
            grid (dict[tuple[int, int], str]): the grid

        Returns:
            int: the result
        """
        x, y = next((x, y) for (x, y), v in grid.items() if v == "@")
        moves = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}
        for move in self.moves:
            dx, dy = moves[move]
            if grid[(x + dx, y + dy)] == "#":
                # hit a wall
                continue
            if grid[(x + dx, y + dy)] == ".":
                # move into clear space
                grid |= {(x, y): ".", (x + dx, y + dy): "@"}
                x, y = x + dx, y + dy
            elif dy == 0:
                # move boxes horizontally
                look = [(x, y), (x + dx, y)]
                while grid[look[-1]] in "[]O":
                    look.append((x + dx * len(look), y))
                if grid[look[-1]] == ".":
                    grid |= {(x, y): "."} | {
                        (x2, y2): grid[(x1, y1)]
                        for (x1, y1), (x2, y2) in pairwise(look)
                    }
                    x, y = x + dx, y + dy
            else:
                # move boxes vertically
                queue = deque([(x + dx, y + dy)])
                moving = {(x, y)}
                while queue:
                    nx, ny = queue.popleft()
                    square = grid[(nx, ny)]
                    queue.extend(
                        (nx + d, ny)
                        for check, d in [("[", 1), ("]", -1)]
                        if square == check and (nx + d, ny) not in moving
                    )
                    if square in "[]O":
                        moving.add((nx, ny))
                        queue.append((nx + dx, ny + dy))
                new_locations = {(bx + dx, by + dy) for bx, by in moving}
                if all(grid[(sx, sy)] == "." for sx, sy in new_locations - moving):
                    grid |= {
                        (bx + dx, by + dy): grid[(bx, by)] for bx, by in moving
                    } | {(bx, by): "." for bx, by in moving - new_locations}
                    x, y = x + dx, y + dy

        return sum(x + 100 * y for (x, y), v in grid.items() if v in "[O")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(self.grid)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(self.expanded_grid)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
