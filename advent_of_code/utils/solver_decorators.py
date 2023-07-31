"""Decorators to help subclasses of the SolverInterface."""
from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def cache_result(func: Callable[P, T]) -> Callable[P, T]:
    """Cache the first call to given function.

    Args:
        func (Callable[P, T]): _description_

    Returns:
        Callable[P, T]: _description_
    """
    has_run = False
    value: T

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        nonlocal has_run
        nonlocal value
        if not has_run:
            value = func(*args, **kwargs)
            has_run = True
        return value

    return wrapper
