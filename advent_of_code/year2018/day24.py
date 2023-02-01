"""Solves the puzzle for Day 24 of Advent of Code 2018.

Immune System Simulator 20XX

For puzzle specification and desciption, visit
https://adventofcode.com/2018/day/24
"""
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, unique
from itertools import count, permutations
from math import ceil
from operator import itemgetter
from pathlib import Path
from re import findall, search
from sys import path
from typing import Dict, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import (
    dataclass_processor,
    enum_re,
    parse_lines,
    split_sections,
)
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


@unique
class AttackType(Enum):
    """Represents the types of attack."""

    radiation = "radiation"
    cold = "cold"
    bludgeoning = "bludgeoning"
    fire = "fire"
    slashing = "slashing"


@dataclass
class Group:
    """Represent a group from the input."""

    units: int
    hp: int
    _impact_str: str
    attack: AttackType
    damage: int
    initiative: int
    _impact_dict: Dict[AttackType, int] = field(default_factory=dict)

    @property
    def effective(self) -> int:
        """The effectiveness of the group.

        Returns:
            int: the effectiveness
        """
        return self.units * self.damage

    @property
    def impact(self) -> Dict[AttackType, int]:
        """The impact for each attack, derived from the _impact_str.

        Returns:
            Dict[AttackType, int]: the impact for each type
        """
        if not self._impact_dict:
            self._impact_dict = {x: 1 for x in AttackType}
            for text, factor in [("immune", 0), ("weak", 2)]:
                if m := search(rf"{text} to ([a-z, ]*)[;)]", self._impact_str):
                    self._impact_dict.update(
                        {
                            AttackType(x): factor
                            for x in findall(rf"({enum_re(AttackType)})", m[1])
                        }
                    )
        return self._impact_dict


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2018
    DAY = 24
    TITLE = "Immune System Simulator 20XX"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input, expected_sections=2)
        self.input = [
            parse_lines(
                section,
                (
                    r"(?P<units>\d+) units each with (?P<hp>\d+) hit points "
                    r"(?P<_impact_str>(\(.*\) )?)"
                    r"with an attack that does (?P<damage>\d+) "
                    rf"(?P<attack>{enum_re(AttackType)}) "
                    r"damage at initiative (?P<initiative>\d+)",
                    dataclass_processor(Group),
                ),
                header=(r"(Immune System:|Infection:)",),
            )
            for section in sections
        ]

        self.immune_system, self.infection = (
            (0, 1) if "Immune System" in sections[0][0] else (1, 0)
        )

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._battle(deepcopy(self.input))

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        result = -1
        for boost in count():
            # keep boosting the immune system army, until it wins a battle
            armies = deepcopy(self.input)
            for group in armies[self.immune_system]:
                group.damage += boost
            self._battle(armies)
            if armies[self.immune_system] and not armies[self.infection]:
                result = sum(group.units for group in armies[self.immune_system])
                break
        return result

    def _battle(self, armies: List[List[Group]]) -> int:
        """Solve part one of the puzzle.

        Args:
            armies (List[List[Group]]): the armies to battle

        Returns:
            int: the answer
        """
        # continue the battle whilst both sides have groups in their armies
        while all(group for group in armies):
            # targetting phase
            targets = []
            for attacker_army, defender_army in permutations(armies):
                attacker_army.sort(
                    key=lambda x: (x.effective, x.initiative), reverse=True
                )
                targetted = [False for _ in defender_army]
                for attacker in attacker_army:
                    target_choices = [
                        (
                            (
                                attacker.units
                                * attacker.damage
                                * defender.impact[attacker.attack],
                                defender.effective,
                                defender.initiative,
                            ),
                            defender_index,
                        )
                        for defender_index, defender in enumerate(defender_army)
                        if not targetted[defender_index]
                        and defender.impact[attacker.attack]
                    ]
                    if target_choices:
                        _, defender_index = max(target_choices, key=itemgetter(0))
                        targets.append((attacker, defender_army[defender_index]))
                        targetted[defender_index] = True

            # attack phase
            targets.sort(key=lambda x: x[0].initiative, reverse=True)
            total_killed = 0
            for attacker, defender in targets:
                if attacker.units >= 1:
                    # the attacker has at least one unit, so can attack
                    killed = min(
                        defender.units,
                        defender.units
                        - ceil(
                            (
                                (defender.units * defender.hp)
                                - (
                                    attacker.units
                                    * attacker.damage
                                    * defender.impact[attacker.attack]
                                )
                            )
                            / defender.hp
                        ),
                    )
                    total_killed += killed
                    defender.units -= killed

                    if defender.units <= 0:
                        # the defender has been defeated, so remove from the battle
                        if defender in armies[0]:
                            armies[0].remove(defender)
                        else:
                            armies[1].remove(defender)

            if total_killed == 0:
                # neither side can kill and win, so exit battle simulation
                break

        # find the winner, and calculate the result
        results = [sum(group.units for group in army) for army in armies]
        return max(results)


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
