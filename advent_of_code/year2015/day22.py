"""Solves the puzzle for Day 22 of Advent of Code 2015.

Wizard Simulator 20XX

For puzzle specification and desciption, visit
https://adventofcode.com/2015/day/22
"""
from enum import Enum, auto
from pathlib import Path
from sys import maxsize, path
from typing import Any, Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import parse_lines, str_tuple_processor
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Spells(Enum):
    """Represents all the spell moves."""

    MAGIC_MISSILE = auto()
    DRAIN = auto()
    SHIELD = auto()
    POISON = auto()
    RECHARGE = auto()


spell_costs = {
    Spells.MAGIC_MISSILE: 53,
    Spells.DRAIN: 73,
    Spells.SHIELD: 113,
    Spells.POISON: 173,
    Spells.RECHARGE: 229,
}

spell_duration = {Spells.SHIELD: 6, Spells.POISON: 6, Spells.RECHARGE: 5}


class Turn(Enum):
    """Who's turn is it anyway?."""

    PLAYER = auto()
    BOSS = auto()


class MinimumValue:
    """Keep track of the minimum of all the values passed through update."""

    value: int

    def __init__(self) -> None:
        """Initialise to the largest possible value."""
        self.value = maxsize

    def update(self, value: int) -> None:
        """Update value, only storing if it is the new minimum.

        Args:
            value (int): The next value
        """
        if value < self.value:
            self.value = value


class Game:
    """The Game simulation, in which a player battles a boss."""

    def __init__(
        self, player_hp: int, cash: int, boss_hp: int, boss_damage: int, hard_mode: bool
    ) -> None:
        """Store the inital settings.

        Args:
            player_hp (int): Players' health points (HP)
            cash (int): the starting cash
            boss_hp (int): the boss' health points (HP)
            boss_damage (int): the boss's starting damage
            hard_mode (bool): True for hard, False for easy

        """
        self.initial_player_hp = player_hp
        self.initial_cash = cash
        self.initial_boss_hp = boss_hp
        self.initial_hard_mode = hard_mode
        self.initial_boss_damage = boss_damage

    def battle(self) -> int:
        """Start the battle.

        Returns:
            int: the the least spent to win
        """
        self.player_hp = self.initial_player_hp
        self.cash = self.initial_cash
        self.boss_hp = self.initial_boss_hp
        self.hard_mode = self.initial_hard_mode
        self.boss_damage = self.initial_boss_damage
        self.spent = 0
        self.armor = 0
        self.depth = 0
        self.effects: Dict[Spells, int] = {}

        # This is a reference to the min value, rather than storing directly
        # as an int, so that it is common to all sub games
        self.best_so_far = MinimumValue()

        self.turn = Turn.PLAYER
        return self._next_turn()

    def _next_turn(self) -> int:
        # have we already found a better result?
        if self.best_so_far.value <= self.spent:
            return maxsize

        # apply effects
        self.armor = 0
        for x in self.effects:
            if x == Spells.SHIELD:
                self.armor = 7
            if x == Spells.POISON:
                self.boss_hp -= 3
            if x == Spells.RECHARGE:
                self.cash += 101
        # reduce effect count by one, and remove if becomes zero
        self.effects = {x: (t - 1) for x, t in self.effects.items() if t > 1}

        # check if the boss is dead from the poison
        if self.boss_hp <= 0:
            self.best_so_far.update(self.spent)
            return self.spent

        # take the turn
        if self.turn == Turn.PLAYER:
            return self._player_turn()
        else:
            return self._boss_turn()

    def _player_turn(self) -> int:
        """Player's turn to attack.

        Returns:
            int: the lowest cash spent
        """
        if self.hard_mode:
            self.player_hp -= 1
            if self.player_hp <= 0:
                return maxsize

        # work out the valid move set
        moves = [
            spell
            for spell, cost in spell_costs.items()
            if (cost <= self.cash) and (spell not in self.effects)
        ]

        # no valid moves
        if len(moves) == 0:
            return maxsize

        # take each move in turn, to find the best next move
        least_spent = maxsize
        for move in moves:
            child = self.spawn_child()
            child.cash -= spell_costs[move]
            child.spent += spell_costs[move]
            if move == Spells.MAGIC_MISSILE:
                child.boss_hp -= 4
            elif move == Spells.DRAIN:
                child.boss_hp -= 2
                child.player_hp += 2
            elif move in spell_duration:
                child.effects[move] = spell_duration[move]

            if child.boss_hp <= 0:
                least_spent = min(least_spent, child.spent)
            else:
                child.depth += 1
                child.turn = Turn.BOSS
                least_spent = min(least_spent, child._next_turn())
        self.best_so_far.update(least_spent)
        return least_spent

    def _boss_turn(self) -> int:
        """Boss's turn to attack.

        Returns:
            int: the lowest cash spent
        """
        self.player_hp -= max(1, self.boss_damage - self.armor)
        if self.player_hp <= 0:
            return maxsize
        self.depth += 1
        self.turn = Turn.PLAYER
        return self._next_turn()

    def spawn_child(self) -> Any:
        """Make a copy of the game.

        Returns:
            Any: Return a copy of self
        """
        obj = type(self).__new__(self.__class__)
        obj.player_hp = self.player_hp
        obj.cash = self.cash
        obj.armor = self.armor
        obj.spent = self.spent
        obj.effects = self.effects.copy()
        obj.boss_hp = self.boss_hp
        obj.depth = self.depth
        obj.hard_mode = self.hard_mode
        obj.boss_damage = self.boss_damage
        obj.best_so_far = self.best_so_far

        return obj


class Solver(SolverInterface):
    """Solution for day 22 of Advent of Code 2015."""

    YEAR = 2015
    DAY = 22
    TITLE = "Wizard Simulator 20XX"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        values = {
            k: int(v)
            for k, v in parse_lines(
                puzzle_input,
                (
                    r"(?P<attr>Hit Points|Damage): (?P<value>[0-9]+)",
                    str_tuple_processor,
                ),
            )
        }
        self.boss_hp = values["Hit Points"]
        self.boss_damage = values["Damage"]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return Game(
            player_hp=50,
            cash=500,
            boss_hp=self.boss_hp,
            boss_damage=self.boss_damage,
            hard_mode=False,
        ).battle()

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return Game(
            player_hp=50,
            cash=500,
            boss_hp=self.boss_hp,
            boss_damage=self.boss_damage,
            hard_mode=True,
        ).battle()


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
