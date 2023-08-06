"""Functions for comparing JSON structures."""
from typing import Any

Json = dict[str, Any] | list[Any] | str | int | float | bool | None


def equals(a: Json, b: Json, skip: list[str]) -> bool:
    """Check for equality between two JSON objects.

    Args:
        a (Json): the first JSON object
        b (Json): the secord JSON object
        skip (list[str]): keys to skip during compare.

    Returns:
        bool: True is equal, otherwise False
    """
    result = True
    if isinstance(a, dict) and isinstance(b, dict):
        # compare dictionaries, catering for skip keys
        for k in a.keys() | b.keys():
            if k not in skip:
                if k in a and k in b:
                    result &= equals(a[k], b[k], skip)
                else:
                    result = False
    elif isinstance(a, list) and isinstance(b, list):
        # compare lists
        if len(a) == len(b):
            result &= all(equals(x, y, skip) for x, y in zip(a, b))
        else:
            result = False
    else:
        result &= a == b
    if not result:
        print()
    return result
