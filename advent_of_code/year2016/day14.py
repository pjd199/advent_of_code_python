"""Solves the puzzle for Day 14 of Advent of Code 2016.

# One-Time Pad

https://adventofcode.com/2016/day/14

## Part One

In order to communicate securely with Santa while you're on this
mission, you've been using a [one-time
pad](https://en.wikipedia.org/wiki/One-time_pad) that you
[generate](https://en.wikipedia.org/wiki/Security_through_obscurity)
using a pre-agreed algorithm. Unfortunately, you've run out of keys in
your one-time pad, and so you need to generate some more.

To generate keys, you first get a stream of random data by taking the
[MD5](https://en.wikipedia.org/wiki/MD5) of a pre-arranged
[salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) (your puzzle
input) and an increasing integer index (starting with `0`, and
represented in decimal); the resulting MD5 hash should be represented as
a string of *lowercase* hexadecimal digits.

However, not all of these MD5 hashes are *keys*, and you need `64` new
keys for your one-time pad. A hash is a key *only if*:

* It contains *three* of the same character in a row, like `777`. Only
  consider the first such triplet in a hash.
* One of the next `1000` hashes in the stream contains that same character
  *five* times in a row, like `77777`.

Considering future hashes for five-of-a-kind sequences does not cause
those hashes to be skipped; instead, regardless of whether the current
hash is a key, always resume testing for keys starting with the very
next hash.

For example, if the pre-arranged salt is `abc`:

* The first index which produces a triple is `18`, because the MD5 hash
  of `abc18` contains `...cc38887a5...`. However, index `18` does not count
  as a key for your one-time pad, because none of the next thousand hashes
  (index `19` through index `1018`) contain `88888`.
* The next index which produces a triple is `39`; the hash of `abc39` contains
  `eee`. It is also the first key: one of the next thousand hashes (the one at
  index 816) contains `eeeee`.
* None of the next six triples are keys, but the one after that, at index `92`,
  is: it contains `999` and index `200` contains `99999`.
* Eventually, index `22728` meets all of the criteria to generate the `64`th key.

So, using our example salt of `abc`, index `22728` produces the `64`th
key.

Given the actual salt in your puzzle input, *what index* produces your
`64`th one-time pad key?

## Part Two

Of course, in order to make this process [even more
secure](https://en.wikipedia.org/wiki/MD5#Security), you've also
implemented [key
stretching](https://en.wikipedia.org/wiki/Key_stretching).

Key stretching forces attackers to spend more time generating hashes.
Unfortunately, it forces everyone else to spend more time, too.

To implement key stretching, whenever you generate a hash, before you
use it, you first find the MD5 hash of that hash, then the MD5 hash of
*that* hash, and so on, a total of *`2016` additional hashings*. Always
use lowercase hexadecimal representations of hashes.

For example, to find the stretched hash for index `0` and salt `abc`:

* Find the MD5 hash of `abc0`: `577571be4de9dcce85a041ba0410f29f`.
* Then, find the MD5 hash of that hash: `eec80a0c92dc8a0777c619d9bb51e910`.
* Then, find the MD5 hash of that hash: `16062ce768787384c81fe17a7a60c7e3`.
* ...repeat many times...
* Then, find the MD5 hash of that hash: `a107ff634856bb300138cac6568c0f24`.

So, the stretched hash for index `0` in this situation is `a107ff...`.
In the end, you find the original hash (one use of MD5), then find the
hash-of-the-previous-hash `2016` times, for a total of `2017` uses of
MD5.

The rest of the process remains the same, but now the keys are entirely
different. Again for salt `abc`:

* The first triple (`222`, at index `5`) has no matching `22222` in the
  next thousand hashes.
* The second triple (`eee`, at index `10`) hash a matching `eeeee` at
  index `89`, and so it is the first key.
* Eventually, index `22551` produces the `64`th key (triple `fff` with
  matching `fffff` at index `22859`.

Given the actual salt in your puzzle input and using `2016` extra MD5
calls of key stretching, *what index* now produces your `64`th one-time
pad key?
"""
from collections import defaultdict
from hashlib import md5
from itertools import count
from multiprocessing import Pool
from pathlib import Path
from re import compile
from sys import path
from typing import Iterator, List

if __name__ == "__main__":  # pragma: no cover
    path.append(str(Path(__file__).parent.parent.parent))

from advent_of_code.utils.runner import runner
from advent_of_code.utils.solver_interface import SolverInterface


def stretch_digest(x: str) -> str:  # pragma: no cover
    """Calculate the stretch digest of the input.

    Args:
        x (str): the input

    Returns:
        str: the stretch digest
    """
    for _ in range(2017):
        x = md5(x.encode()).hexdigest()  # nosec
    return x


class Solver(SolverInterface):
    """Solves the puzzle."""

    YEAR = 2016
    DAY = 14
    TITLE = "One-Time Pad"

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
        pattern = compile(r"\w+")
        for i, line in enumerate(puzzle_input):
            if m := pattern.fullmatch(line):
                self.input = m[0]
            else:
                raise RuntimeError(f"Unable to parse {line} on line {i+1}")

    def solve_part_one(self) -> int:
        """Solve part one of the puzzle.

        Returns:
            int: the answer
        """
        return self._find(
            (md5(f"{self.input}{j}".encode()).hexdigest() for j in count()),  # nosec
        )

    def solve_part_two(self) -> int:
        """Solve part two of the puzzle, with multiprocessing speed boost.

        Returns:
            int: the answer
        """
        with Pool() as pool:
            return self._find(
                pool.imap(stretch_digest, (f"{self.input}{j}" for j in count()), 500)
            )

    def _find(self, iterator: Iterator[str]) -> int:
        """Search for the answers.

        Args:
            iterator (Iterator[str]): the iterator for the MD5 hash stream

        Returns:
            int: the index after 64 successful 5* hashes
        """
        list_of_threes = defaultdict(list)
        pattern_three = compile(r"(.)\1\1")
        pattern_five = compile(r"(.)\1\1\1\1")

        found = 0
        result = -1
        i = -1

        while found < 64:
            i += 1
            digest = next(iterator)

            # check for three repeated characters
            if m := pattern_three.search(digest):
                list_of_threes[m[1]].append(i)

            # check for five repeated characters
            if m := pattern_five.search(digest):
                threes = [x for x in list_of_threes[m[1]] if (i - 1000) < x < i]
                for j in threes:
                    found += 1
                    if found == 64:
                        result = j
                        break
        return result


if __name__ == "__main__":  # pragma: no cover
    runner(Solver)
