"""Functions for comparing JSON structures."""
from typing import Any, Optional


def json_equals(a: Any, b: Any, ignore: Optional[tuple[str, ...]]) -> bool:
    """Check for equality between two JSON objects.

    Args:
        a (Any): the first JSON object
        b (Any): the secord JSON object
        ignore (tuple[str] | None): keys to ignore during compare. Defaults to None.

    Returns:
        bool: True is equal, otherwise False
    """
    result = True
    if isinstance(a, dict) and isinstance(b, dict):
        # compare dictionaries, catering for ignore keys
        for k in a.keys() | b.keys():
            if ignore and k not in ignore:
                if k in a and k in b:
                    result &= json_equals(a[k], b[k], ignore)
                else:
                    result = False
    elif isinstance(a, list) and isinstance(b, list):
        # compare lists
        if len(a) == len(b):
            result &= all(json_equals(x, y, ignore) for x, y in zip(a, b))
        else:
            result = False
    else:
        result &= a == b

    return result
