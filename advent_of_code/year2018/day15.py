"""Solves the puzzle for Day 15 of Advent of Code 2018.

Beverage Bandits

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/15
"""
from collections import deque
from copy import deepcopy
from itertools import count
from pathlib import Path
from sys import path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_tokens, str_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 15
    TITLE = "Beverage Bandits"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        # parse the rules
        self.input = parse_tokens(puzzle_input, (r"[#.EG]", str_processor))

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        outcome, _, _ = self._solve(3)
        return outcome

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        elf_count = sum(1 for row in self.input for value in row if value == "E")
        result = -1
        # loop with increasing power until all elves survive
        for elf_attack_power in count(4):
            outcome, winner, survivors = self._solve(elf_attack_power)
            if winner == "E" and survivors == elf_count:
                result = outcome
                break

        return result

    def _solve(self, elf_power: int) -> tuple[int, str, int]:
        """Solve the battle by simulating a battle.

        Args:
            elf_power (int): the attack power for the elf

        Returns:
            tuple[int, str, int]: (outcome score, winner, survivor count)
        """
        self.grid = deepcopy(self.input)
        self.elf_power = elf_power
        self.units = {
            (x, y): 200
            for y, row in enumerate(self.grid)
            for x, value in enumerate(row)
            if value in "EG"
        }

        # simulate the battle
        self.units_in_this_round: deque[tuple[int, int]] = deque()
        completed_rounds = -1
        while True:
            # check for end of round
            if not self.units_in_this_round:
                # start next round
                completed_rounds += 1
                self.units_in_this_round.extend(
                    sorted(self.units.keys(), key=lambda a: (a[1], a[0]))
                )

            # check for end of battle condition
            if len({self.grid[y][x] for x, y in self.units.keys()}) == 1:
                break

            # select next unit
            x, y = self.units_in_this_round.popleft()

            # move the unit, if possible
            x, y = self._move(x, y)

            # attack enemy if possible
            self._attack(x, y)

        # battle complete, return the vital stats
        survivors = [self.grid[y][x] for x, y in self.units.keys()]
        return (
            completed_rounds * sum(self.units.values()),
            survivors[0],
            len(survivors),
        )

    def _move(self, unit_x: int, unit_y: int) -> tuple[int, int]:
        """Move the unit at the given co-ordinates, and return the new co-ordinates.

        Args:
            unit_x (int): x co-ordinate
            unit_y (int): y co-ordinate

        Returns:
            tuple[int, int]: the new x,y co-ordinates
        """
        enemy_type = "G" if self.grid[unit_y][unit_x] == "E" else "E"
        if not _adjacent_values(unit_x, unit_y, enemy_type, self.grid):
            # perform a breadth first search to find the shortest paths
            # to the square in range of attack
            queue: deque[tuple[int, int, list[tuple[int, int]]]] = deque([])
            queue.append((unit_x, unit_y, []))
            visited = {(unit_x, unit_y)}
            paths = []
            squares_in_range = {
                (adj_x, adj_y)
                for x, y in self.units.keys()
                for adj_x, adj_y in _adjacent_values(x, y, ".", self.grid)
                if self.grid[y][x] == enemy_type
            }
            while queue:
                x, y, path = queue.popleft()
                for move_x, move_y in _adjacent_values(x, y, ".", self.grid):
                    if (move_x, move_y) not in visited:
                        visited.add((move_x, move_y))
                        queue.append((move_x, move_y, path + [(move_x, move_y)]))
                        if (move_x, move_y) in squares_in_range:
                            paths.append(path + [(move_x, move_y)])
                if len(paths) > 2 and len(paths[0]) != len(paths[-1]):
                    # found shortest path with no tie break, so stop search early
                    break

            if paths:
                # able to move, so select the closest and move the unit
                paths.sort(key=lambda a: (len(a), a[-1][1], a[-1][0], a[0][1], a[0][0]))
                new_x, new_y = paths[0][0]
                self.grid[new_y][new_x] = self.grid[unit_y][unit_x]
                self.units[(new_x, new_y)] = self.units[(unit_x, unit_y)]
                self.grid[unit_y][unit_x] = "."
                del self.units[(unit_x, unit_y)]
                unit_x, unit_y = new_x, new_y

        return unit_x, unit_y

    def _attack(self, unit_x: int, unit_y: int) -> None:
        """Attack!!!

        Args:
            unit_x (int): x co-ordinate of the attacking unit
            unit_y (int): y co-ordinate of the attacking unit
        """
        enemy_type = "G" if self.grid[unit_y][unit_x] == "E" else "E"

        targets = _adjacent_values(unit_x, unit_y, enemy_type, self.grid)
        if targets:
            targets.sort(key=lambda a: (self.units[(a[0], a[1])], a[1], a[0]))
            target = targets[0]
            self.units[target] -= self.elf_power if enemy_type == "G" else 3
            if self.units[target] <= 0:
                # target killed
                self.grid[target[1]][target[0]] = "."
                del self.units[target]
                if target in self.units_in_this_round:
                    self.units_in_this_round.remove(target)


def _adjacent_values(
    x: int, y: int, value: str, grid: list[list[str]]
) -> list[tuple[int, int]]:
    return [
        (a, b)
        for a, b in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        if grid[b][a] == value
    ]


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
