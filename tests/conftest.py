"""Fixtures shared accross the test suite."""
from typing import Any

import pytest


def check_json(
    left: dict[str, Any],
    right: dict[str, Any],
    skip: list[str] | None = None,
    replace: list[tuple[str, str]] | None = None,
    path: str = "$",
) -> None:
    """Check for equality between two JSON objects.

    Args:
        left (dict[str, Any]): the left JSON object
        right (dict[str, Any]): the right JSON object
        skip (list[str] | None): keys to skip during compare.
        replace(list[tuple[str, str]] | None): strings to replace during compare
        path (str): path to track recursion
    """
    if isinstance(left, dict) and isinstance(right, dict):
        # compare dictionaries, catering for skip keys
        for key in left.keys() | right.keys():
            if skip is None or key not in skip:
                assert key in left, f"{key} is not in left at {path}"
                assert key in right, f"{key} is not in right at {path}"
                check_json(left[key], right[key], skip, replace, f"{path}['{key}']")
    elif isinstance(left, list) and isinstance(right, list):
        # compare lists
        assert len(left) == len(
            right
        ), f"List length mismatch ({len(left)} != {len(right)}) at {path}"
        for i, (x, y) in enumerate(zip(left, right)):
            check_json(x, y, skip, replace, f"{path}['{i}']")
    elif replace is not None and isinstance(left, str) and isinstance(right, str):
        # compare strings, with replacement
        left1, right1 = left, right
        for old, new in replace:
            left1 = left1.replace(old, new)
            right1 = right1.replace(old, new)
        assert left1 == right1, f"{left} != {right} at {path}\n{left1} != {right1}"
    else:
        # compare other types
        assert left == right, f"{left} != {right} at {path}"


# export check_json into the pytest namespace
pytest.check_json = check_json
