"""Decorators for the SolverInterface."""
from collections.abc import Callable
from typing import TypeVar

from advent_of_code.utils.solver_interface import SolverInterface

S = TypeVar("S", bound=SolverInterface)
T = TypeVar("T")


def cache_result(func: Callable[[S], T]) -> Callable[[S], T]:
    """Method decorator to cache results.

    Args:
        func (Callable[[S], T]): the method

    Returns:
        Callable[[S], T]: decorated method
    """

    def wrapper(instance: S) -> T:
        cache = instance.__dict__.setdefault("__result_cache__", {})

        if func not in cache:
            cache[func] = func(instance)

        result: T = cache[func]
        return result

    return wrapper
