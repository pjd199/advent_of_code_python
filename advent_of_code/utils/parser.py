"""Parser utilities for the puzzle input."""
from dataclasses import fields
from enum import Enum
from re import escape, fullmatch, search, split
from sys import maxsize
from typing import Callable, Dict, List, Match, Tuple, Type, TypeVar, Union

T = TypeVar("T")


def int_processor(match: Match[str]) -> int:
    """Process match object as an int.

    Args:
        match (Match[str]): the regular expression Match

    Returns:
        int: the result
    """
    return int(match[0])


def int_processor_group(group: Union[str, int]) -> Callable[[Match[str]], int]:
    """Process match object as a str.

    Args:
        group (Union[str, int]): the group name of numvber to match

    Returns:
        str: the result
    """
    return lambda m: int(m.group(group))


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


def str_processor_group(group: Union[str, int]) -> Callable[[Match[str]], str]:
    """Process match object as a str.

    Args:
        group (Union[str, int]): the group name of numvber to match

    Returns:
        str: the result
    """
    return lambda m: m.group(group)


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
    enum: Type[T],
) -> Callable[[Match[str]], T]:
    """Create a match processor to process match object as a data class.

    Args:
        enum (Type[T]): the enum to initialise

    Raises:
        ValueError: if T is not a subclass of Enum

    Returns:
        Callable[[Match[str]], T]: the match processor
    """
    if any(cls == Enum for cls in enum.__bases__):
        return lambda m: enum(m[0])  # type: ignore [call-arg]
    else:
        raise ValueError("argument must be subclass of Enum")


def enum_re(enumeration: Type[Enum]) -> str:
    """Syntactic sugar for using Enum's in regular expressions.

    Args:
        enumeration (Type[Enum]): the enum to use

    Returns:
        str: list of values in the enum, delimited by a "|"
    """
    return "|".join(
        sorted([escape(str(x.value)) for x in enumeration], key=len, reverse=True)
    )


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
        if not fullmatch(header[start], puzzle_input[start]):
            raise RuntimeError(
                f"Unable to parse '{puzzle_input[start]}' on line {start + 1}"
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
            raise RuntimeError(f"Unable to parse '{line}' on line {i + 1}: {e}")

    return output


def parse_single_line(
    puzzle_input: List[str],
    pattern: str,
    match_processor: (Callable[[Match[str]], T]),
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
    *args: Tuple[str, Callable[[Match[str]], T]],
    delimiter: str = "",
    require_delimiter: bool = True,
    min_length: int = 1,
    max_length: int = maxsize,
    header: Tuple[str, ...] = (),
) -> List[List[T]]:
    """Load lines using the tokenised methods.

    Args:
        puzzle_input (List[str]): the puzzle input
        *args: Tuple[str, Callable[[Match[str]], T]]: processors called for each match
        delimiter (str): the delimiter expected between tokens. Defaults to "".
        require_delimiter (bool): delimiter must be present when True. Defaults to True.
        min_length (int): the minimum number of lines expected. Defaults to 1.
        max_length (int): the maximum number of lines expected. Defaults to maxsize.
        header (Tuple[str, ...], optional): header to validate. Defaults to ().

    Raises:
        RuntimeError: if the input has an invalid pattern and delimiter combination

    Returns:
        List[List[T]]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # parse the input
    output: List[List[T]] = []
    for i, line in enumerate(puzzle_input[start:]):
        # check for at least one delimiter on the line
        if line == "" or (require_delimiter and not search(delimiter, line)):
            raise RuntimeError(
                f"Unable to parse '{line}' on line {i + 1}:"
                f" Delimiter '{delimiter}' not found"
            )

        # parse each token on the line
        output.append([])
        if delimiter == "":
            tokens = list(line)
        else:
            tokens = [x for x in split(delimiter, line) if x != ""]
        for token in tokens:
            try:
                # search for a matching pattern
                found = False
                for pattern, match_processor in args:
                    if m := fullmatch(pattern, token):
                        output[-1].append(match_processor(m))
                        found = True
                        break
                if not found:
                    raise RuntimeError("No match found")
            except Exception as e:
                raise RuntimeError(f"Unable to parse '{line}' on line {i + 1}: {e}")

    return output


def parse_tokens_single_line(
    puzzle_input: List[str],
    *args: Tuple[str, Callable[[Match[str]], T]],
    delimiter: str = "",
    require_delimiter: bool = True,
    header: Tuple[str, ...] = (),
) -> List[T]:
    """Load lines using the tokenised methods.

    Args:
        puzzle_input (List[str]): the puzzle input
        *args: Tuple[str, Callable[[Match[str]], T]]: processors called for each match
        delimiter (str): the delimiter expected between tokens. Defaults to "".
        header (Tuple[str, ...], optional): header to validate. Defaults to ().

    Returns:
        List[T]: the parsed output
    """
    return parse_tokens(
        puzzle_input,
        *args,
        delimiter=delimiter,
        require_delimiter=require_delimiter,
        min_length=1,
        max_length=1,
        header=header,
    )[0]


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
            raise RuntimeError(f"Unable to parse '{line}' on line {y + 1}")
        for x, char in enumerate(line):
            try:
                if m := fullmatch(pattern, char):
                    output[(x, y)] = match_processor(m)
                else:
                    raise RuntimeError(
                        f"No match with {pattern} for "
                        f"character '{char}' at position {x}"
                    )
            except Exception as e:
                raise RuntimeError(f"Unable to parse '{line}' on line {y + 1}: {e}")

    return output


def split_sections(
    puzzle_input: List[str],
    section_break: str = "",
    expected_sections: int = maxsize,
    min_length: int = 1,
    max_length: int = maxsize,
    header: Tuple[str, ...] = (),
) -> List[List[str]]:
    """Split the input into sections where a lines matches the section_break regex.

    Args:
        puzzle_input (List[str]): the puzzle input
        section_break (str): the section break regex
        expected_sections (int): the number of sections to expect.
        min_length (int): the minimum number of lines expected
        max_length (int): the maximum number of lines expected
        header (Tuple[str, ...], optional): header to validate. Default ()

    Raises:
        RuntimeError: if the puzzle_input has incorrect length or number of sections

    Returns:
        List[T]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # parse the input into sections
    output: List[List[str]] = []
    section: List[str] = []
    for line in puzzle_input[start:]:
        if fullmatch(section_break, line):
            if section:
                output.append(section)
                section = []
        else:
            section.append(line)
    output.append(section)

    if expected_sections < maxsize and len(output) != expected_sections:
        raise RuntimeError(
            f"Found {len(output)} sections, expected {expected_sections}"
        )

    return output
