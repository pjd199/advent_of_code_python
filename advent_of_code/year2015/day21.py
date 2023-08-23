"""Solves the puzzle for Day 21 of Advent of Code 2015.

RPG Simulator 20XX

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/21
"""
from collections import namedtuple
from itertools import combinations
from pathlib import Path
from sys import maxsize, path

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_decorators import cache_result
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solve the puzzle for the day."""

    YEAR = 2015
    DAY = 21
    TITLE = "RPG Simulator 20XX"

    def __init__(self, puzzle_input: list[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (list[str]): The lines of the input file
        """
        values = {
            k: int(v)
            for k, v in parse_lines(
                puzzle_input,
                (
                    r"(?P<attr>Hit Points|Damage|Armor): (?P<value>[0-9]+)",
                    str_tuple_processor,
                ),
            )
        }
        self.boss_hp = values["Hit Points"]
        self.boss_damage = values["Damage"]
        self.boss_armor = values["Armor"]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        least_to_win, _ = self._battle()
        return least_to_win

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        _, most_to_lose = self._battle()
        return most_to_lose

    @cache_result
    def _battle(self) -> tuple[int, int]:
        """Fight.

        Returns:
            tuple[int, int]: results of the two parts
        """
        Item = namedtuple("Item", ["cost", "damage", "armor"])

        weapon_list = [
            Item(8, 4, 0),  # dagger
            Item(10, 5, 0),  # short sword
            Item(25, 6, 0),  # warhammer
            Item(40, 7, 0),  # long sword
            Item(74, 8, 0),  # great axe
        ]

        armor_list = [
            Item(0, 0, 0),  # no armor
            Item(13, 0, 1),  # leather
            Item(31, 0, 2),  # chain mail
            Item(53, 0, 3),  # splint mail
            Item(75, 0, 4),  # banded mail
            Item(102, 0, 5),  # plate mail
        ]

        ring_list = [
            Item(0, 0, 0),  # no ring
            Item(0, 0, 0),  # no ring
            Item(25, 1, 0),  # damage +1
            Item(50, 2, 0),  # damage +2
            Item(100, 3, 0),  # damage +3
            Item(20, 0, 1),  # armor +1
            Item(40, 0, 2),  # armor +2
            Item(80, 0, 3),  # armor +3
        ]

        # for each purchase posiblity, simulate the battle and record result
        least_to_win = maxsize
        most_to_lose = 0
        for weapon in weapon_list:
            for armor in armor_list:
                for ring1, ring2 in combinations(ring_list, 2):
                    player_points = 100  # player always starts with 100
                    boss_points = self.boss_hp

                    player_damage = (
                        weapon.damage + armor.damage + ring1.damage + ring2.damage
                    )
                    player_armor = (
                        weapon.armor + armor.armor + ring1.armor + ring2.armor
                    )
                    cost = weapon.cost + armor.cost + ring1.cost + ring2.cost

                    # simulate the battle
                    while True:
                        # player attacks first
                        boss_points -= max(1, player_damage - self.boss_armor)
                        if boss_points <= 0:
                            # player wins
                            least_to_win = min(least_to_win, cost)
                            break
                        # boss attacks
                        player_points -= max(1, self.boss_damage - player_armor)
                        if player_points <= 0:
                            # boss wins
                            most_to_lose = max(most_to_lose, cost)
                            break

        return least_to_win, most_to_lose


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
