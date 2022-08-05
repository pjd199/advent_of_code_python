"""Solves the puzzle for Day 17 of Advent of Code 2016.

# Two Steps Forward

https://adventofcode.com/2016/day/17

## Part One

You're trying to access a secure vault protected by a `4x4` grid of
small rooms connected by doors. You start in the top-left room (marked
`S`), and you can access the vault (marked `V`) once you reach the
bottom-right room:

```
#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |
####### V

```

Fixed walls are marked with `#`, and doors are marked with `-` or `|`.

The doors in your *current room* are either open or closed (and locked)
based on the hexadecimal [MD5](https://en.wikipedia.org/wiki/MD5) hash
of a passcode (your puzzle input) followed by a sequence of uppercase
characters representing the *path you have taken so far* (`U` for up,
`D` for down, `L` for left, and `R` for right).

Only the first four characters of the hash are used; they represent,
respectively, the doors *up, down, left, and right* from your current
position. Any `b`, `c`, `d`, `e`, or `f` means that the corresponding
door is *open*; any other character (any number or `a`) means that the
corresponding door is *closed and locked*.

To access the vault, all you need to do is reach the bottom-right room;
reaching this room opens the vault and all doors in the maze.

For example, suppose the passcode is `hijkl`. Initially, you have taken
no steps, and so your path is empty: you simply find the MD5 hash of
`hijkl` alone. The first four characters of this hash are `ced9`, which
indicate that up is open (`c`), down is open (`e`), left is open (`d`),
and right is closed and locked (`9`). Because you start in the top-left
corner, there are no 'up' or 'left' doors to be open, so your only
choice is *down*.

Next, having gone only one step (down, or `D`), you find the hash of
`hijkl*D*`. This produces `f2bc`, which indicates that you can go back
up, left (but that's a wall), or right. Going right means hashing
`hijkl*DR*` to get `5745` - all doors closed and locked. However, going
*up* instead is worthwhile: even though it returns you to the room you
started in, your path would then be `DU`, opening a *different set of
doors*.

After going `DU` (and then hashing `hijkl*DU*` to get `528e`), only the
right door is open; after going `DUR`, all doors lock. (Fortunately,
your actual passcode is not `hijkl`).

Passcodes actually used by Easter Bunny Vault Security do allow access
to the vault if you know the right path. For example:

* If your passcode were `ihgpwlah`, the shortest path would be `DDRRRD`.
* With `kglvqrro`, the shortest path would be `DDUDRLRRUDRD`.
* With `ulqzkmiv`, the shortest would be `DRURDRUDDLLDLUURRDULRLDUUDDDRR`.

Given your vault's passcode, *what is the shortest path* (the actual
path, not just the length) to reach the vault?

## Part Two

You're curious how robust this security solution really is, and so you
decide to find longer and longer paths which still provide access to the
vault. You remember that paths always end the first time they reach the
bottom-right room (that is, they can never pass through it, only end in
it).

For example:

* If your passcode were `ihgpwlah`, the longest path would take `370` steps.
* With `kglvqrro`, the longest path would be `492` steps long.
* With `ulqzkmiv`, the longest path would be `830` steps long.

What is the *length of the longest path* that reaches the vault?
"""
from collections import deque
from hashlib import md5
from pathlib import Path
from re import compile
from sys import path
from typing import Deque, List, Tuple

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 17
    TITLE = "Two Steps Forward"

    def __init__(self, puzzle_input: List[str]) -> None:
        """Initialise the puzzle and parse the input.

        Args:
            puzzle_input (List[str]): The lines of the input file

        Raises:
            RuntimeError: Raised if the input cannot be parsed
        """
        # validate and parse the input
        if (
            puzzle_input is None
            or len(puzzle_input) == 0
            or len(puzzle_input[0].strip()) == 0
        ):
            raise RuntimeError("Puzzle input is empty")

        # parse the input
        pattern = compile(r"[a-z]+")
        for i, line in enumerate(puzzle_input):
            if (m := pattern.fullmatch(line)) and (i == 0):
                self.input = m[0]
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

        self.run = False

    def solve_part_one(self) -> str:
        """Solve part one of the puzzle.

        Returns:
            str: the answer
        """
        self._run()
        return self.shortest

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle.

        Returns:
            int: the answer
        """
        self._run()
        return len(self.longest)

    def _run(self) -> None:
        """Run the simulation."""
        if self.run:
            return

        queue: Deque[Tuple[int, int, str]] = deque([(0, 0, "")])

        moves = {
            "U": (0, -1),
            "D": (0, +1),
            "L": (-1, 0),
            "R": (+1, 0),
        }

        shortest = " " * 10000
        longest = ""
        while queue:
            x, y, path = queue.popleft()

            if (x, y) == (3, 3):
                if len(path) < len(shortest):
                    shortest = path
                if len(path) > len(longest):
                    longest = path
                continue

            for i, (direction, move) in enumerate(moves.items()):
                new_path = f"{path}{direction}"
                new_x, new_y = x + move[0], y + move[1]
                if (
                    0 <= new_x < 4
                    and 0 <= new_y < 4
                    and md5(f"{self.input}{path}".encode()).hexdigest()[i]  # nosec
                    in "bcdef"
                ):
                    queue.append((new_x, new_y, new_path))

        self.shortest = shortest
        self.longest = longest
        self.run = True


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
