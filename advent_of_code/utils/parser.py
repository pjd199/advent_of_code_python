"""Parser utilities for the puzzle input."""
from dataclasses import fields
from enum import Enum
from re import finditer, fullmatch, sub
from sys import maxsize
from typing import Callable, Dict, List, Match, Tuple, Type, TypeVar

T = TypeVar("T")


def int_processor(match: Match[str]) -> int:
    """Process match object as an int.

    Args:
        match (Match[str]): the regular expression Match

    Returns:
        int: the result
    """
    return int(match[0])


def int_tuple_processor(match: Match[str]) -> Tuple[int, ...]:
    """Process match object as an int tuple.

    Args:
        match (Match[str]): the regular expression Match[str]

    Returns:
        Tuple[int,...]: the result
    """
    return tuple(int(x) for x in match.groups())


def str_processor(match: Match[str]) -> str:
    """Process match object as a str.

    Args:
        match (Match[str]): the regular expression Match

    Returns:
        str: the result
    """
    return match[0]


def str_tuple_processor(match: Match[str]) -> Tuple[str, ...]:
    """Process match object as a str tuple.

    Args:
        match (Match[str]): the regular expression Match

    Returns:
        Tuple[str, ...]: the result
    """
    return match.groups()


def dataclass_processor(
    cls: Type[T],
) -> Callable[[Match[str]], T]:
    """Create a match processor to process match object as a data class.

    Args:
        cls (Type[T]): the data class to initialise

    Returns:
        Callable[[Match[str]], T]: the match processor
    """
    fields_dict = {f.name: f for f in fields(cls) if f.init}
    return lambda m: cls(
        **{
            k: fields_dict[k].type(v)
            for k, v in m.groupdict().items()
            if k in fields_dict and v is not None
        }
    )


def enum_processor(
    enum: Type[Enum],
) -> Callable[[Match[str]], Enum]:
    """Create a match processor to process match object as a data class.

    Args:
        enum (Enum): the enum to initialise

    Returns:
        Callable[[Match[str]], Enum]: the match processor
    """
    return lambda m: enum(m[0])


def _validate_input_and_header(
    puzzle_input: List[str],
    min_length: int,
    max_length: int,
    header: Tuple[str, ...],
) -> int:
    """Validates the input.

    Args:
        puzzle_input (List[str]): the puzzle input
        min_length (int): the minimum allowable length
        max_length (int): the maximum allowable length
        header (Tuple[str, ...], optional): header to validate. Default ()

    Raises:
        RuntimeError: raised on invalid puzzle_input

    Returns:
        int: the start line of the data, after the header
    """
    # validate puzzle_input
    if puzzle_input is None or not (min_length <= len(puzzle_input) <= max_length):
        raise RuntimeError("Input is None or of incorrect length")

    # validate the optional header
    start = 0
    while start < len(header):
        if puzzle_input[start] != header[start]:
            raise RuntimeError(
                f"Unable to parse {puzzle_input[start]} " f"on line {start + 1}"
            )
        start += 1

    return start


def parse_lines(
    puzzle_input: List[str],
    *args: Tuple[str, Callable[[Match[str]], T]],
    min_length: int = 1,
    max_length: int = maxsize,
    header: Tuple[str, ...] = (),
) -> List[T]:
    """Load lines from the parsed patterns.

    Args:
        puzzle_input (List[str]): the puzzle input
        *args: Tuple[str, Callable[[Match[str]], T]]: processors called for each match
        min_length (int): the minimum number of lines expected
        max_length (int): the maximum number of lines expected
        header (Tuple[str, ...], optional): header to validate. Default ()

    Raises:
        RuntimeError: if the puzzle_input has the wrong length

    Returns:
        List[T]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # parse the input
    output: List[T] = []
    for i, line in enumerate(puzzle_input[start:]):
        try:
            found = False
            for pattern, match_processor in args:
                if m := fullmatch(pattern, line):
                    output.append(match_processor(m))
                    found = True
                    break
            if not found:
                raise RuntimeError("No match found")
        except Exception as e:
            raise RuntimeError(f"Unable to parse {line} on line {i + 1}: {e}")

    return output


def parse_single_line(
    puzzle_input: List[str],
    pattern: str,
    match_processor: Callable[[Match[str]], T],
) -> T:
    """Load lines from the parsed patterns.

    Args:
        puzzle_input (List[str]): the puzzle input
        pattern (str): the regular expression pattern for each line
        match_processor (Callable[[Match[str]], T]): processor called for the match

    Returns:
        T: _description_
    """
    return parse_lines(
        puzzle_input,
        (pattern, match_processor),
        min_length=1,
        max_length=1,
    )[0]


def parse_tokens(
    puzzle_input: List[str],
    pattern: str,
    match_processor: Callable[[Match[str]], T],
    delimiter: str = "",
    min_length: int = 1,
    max_length: int = maxsize,
    header: Tuple[str, ...] = (),
) -> List[List[T]]:
    """Load lines using the tokenised methods.

    Args:
        puzzle_input (List[str]): the puzzle input
        pattern (str): the regular expression pattern for each token
        match_processor (Callable[[Match[str]], T]): processor called for the match
        delimiter (str): the delimiter expected between tokens. Defaults to "".
        min_length (int): the minimum number of lines expected. Defaults to 1.
        max_length (int): the maximum number of lines expected. Defaults to maxsize.
        header (Tuple[str, ...], optional): header to validate. Defaults to ().

    Raises:
        RuntimeError: if the input has an invalid pattern and delimiter combination

    Returns:
        List[List[T]]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # check for a valid delimiter pattern
    line_pattern = rf"{pattern}({delimiter}{pattern})+"
    line_pattern = sub(r"\(\?P<[a-z]+>", lambda x: r"(", line_pattern)
    for i, line in enumerate(puzzle_input[start:]):
        try:
            if not fullmatch(line_pattern, line):
                raise RuntimeError("No match for pattern with delimiter")
        except Exception as e:
            raise RuntimeError(
                f"Unable to validate {line} on line {i + 1} with {line_pattern}: {e}"
            )

    # parse the input
    output: List[List[T]] = []
    for i, line in enumerate(puzzle_input[start:]):
        try:
            output.append([match_processor(m) for m in finditer(pattern, line)])
            if not output[-1]:
                raise RuntimeError("No match")
        except Exception as e:
            raise RuntimeError(f"Unable to parse {line} on line {i + 1}: {e}")

    return output


def parse_grid(
    puzzle_input: List[str],
    pattern: str,
    match_processor: Callable[[Match[str]], T],
    min_length: int = 1,
    max_length: int = maxsize,
    header: Tuple[str, ...] = (),
) -> Dict[Tuple[int, int], T]:
    """Load lines as an x y grid and initialise classes with the whole pattern match.

    Args:
        puzzle_input (List[str]): the puzzle input
        match_processor (Callable[[Match[str]], T]]): processor called for the match
        pattern (str): the regular expression pattern for each line
        min_length (int): the minimum number of lines expected
        max_length (int): the maximum number of lines expected
        header (Tuple[str, ...]): header to validate. Default ()

    Raises:
        RuntimeError: if the puzzle_input has the wrong length

    Returns:
        Dict[Tuple[int, int], T]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # parse the input
    output: Dict[Tuple[int, int], T] = {}
    for y, line in enumerate(puzzle_input[start:]):
        if not line:
            raise RuntimeError(f"Unable to parse {line} on line {y + 1}")
        for x, char in enumerate(line):
            try:
                if m := fullmatch(pattern, char):
                    output[(x, y)] = match_processor(m)
                else:
                    raise RuntimeError("No match")
            except Exception as e:
                raise RuntimeError(f"Unable to parse {line} on line {y + 1}: {e}")

    return output
