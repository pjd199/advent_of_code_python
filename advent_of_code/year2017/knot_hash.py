"""Knot Hash function."""
from functools import reduce
from itertools import chain
from operator import xor


def knot_hash(text: str) -> str:
    """Calculate the Knot Hash for the given input string.

    Args:
        text (str): the input string

    Returns:
        str: the hash result, as a hexidecimal string
    """
    data = list(range(256))
    position = 0
    skip = 0
    for _ in range(64):
        for length in chain([ord(c) for c in text], [17, 31, 73, 47, 23]):
            section = [data[i % len(data)] for i in range(position, position + length)]
            for i, x in enumerate(reversed(section)):
                data[(position + i) % len(data)] = x
            position += length + skip
            skip += 1

    dense_hash = [reduce(xor, data[i : i + 16]) for i in range(0, 256, 16)]

    return "".join(f"{x:02x}" for x in dense_hash)
