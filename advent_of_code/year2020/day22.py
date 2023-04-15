"""Solves the puzzle for Day 22 of Advent of Code 2020.

Crab Combat

For puzzle specification and desciption, visit
https://adventofcode.com/2020/day/22
"""
from collections import deque
from itertools import islice
from pathlib import Path
from sys import path
from typing import Deque, List, Set, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.parser import int_processor, parse_lines, split_sections
from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2020
    DAY = 22
    TITLE = "Crab Combat"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file
        """
        sections = split_sections(puzzle_input, expected_sections=2)
        self.input = [
            parse_lines(section, (r"\d+", int_processor), header=(f"Player {i+1}:",))
            for i, section in enumerate(sections)
        ]

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(recursive_combat=False)

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        return self._solve(recursive_combat=True)

    def _solve(self, recursive_combat: bool) -> int:
        """Solve the puzzle.

        Args:
            recursive_combat (bool): if True, enable recursive game play

        Returns:
            int: the winner (0 for player 1, 1 for player 2)
        """
        players = [deque(hand) for hand in self.input]
        winner = self._game(players, recursive_combat)
        return sum((i + 1) * card for i, card in enumerate(reversed(players[winner])))

    def _game(self, players: List[Deque[int]], recursive_combat: bool) -> int:
        """Play the game.

        Args:
            players (List[Deque[int]]): the player's hands
            recursive_combat (bool): if True, enable recursive game play

        Returns:
            int: the winner (0 for player 1, 1 for player 2)
        """
        history: Set[Tuple[Tuple[int, ...], Tuple[int, ...]]] = set()
        game_winner = -1

        # keep playing rounds until a player wins the game
        while True:
            # check for infinite loops by detecting moments in history
            moment = (tuple(players[0]), tuple(players[1]))
            if moment in history:
                game_winner = 0
                break
            history.add(moment)

            # play the top card
            play = [players[0].popleft(), players[1].popleft()]
            if (
                recursive_combat
                and len(players[0]) >= play[0]
                and len(players[1]) >= play[1]
            ):
                # round winner determined by recursive play (when enabled)
                round_winner = self._game(
                    [
                        deque(islice(players[0], 0, play[0])),
                        deque(islice(players[1], 0, play[1])),
                    ],
                    recursive_combat,
                )

            else:
                # round winner determined by highest card
                round_winner = 0 if play[0] > play[1] else 1

            # winner takes the cards
            players[round_winner].append(play[round_winner])
            players[round_winner].append(play[1 - round_winner])

            if len(players[0]) == 0 or len(players[1]) == 0:
                game_winner = 1 if players[1] else 0
                break

        return game_winner


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
