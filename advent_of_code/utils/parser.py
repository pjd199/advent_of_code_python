"""Parser utilities for the puzzle input."""
from builtins import type
from collections.abc import Callable
from dataclasses import fields, is_dataclass
from enum import Enum
from re import Match, escape, fullmatch, search, split
from sys import maxsize
from typing import TypeVar

T = TypeVar("T")


class ParseError(Exception):
    """Raised when there is a problem with parsing."""

    def __init__(
        self, message: str, text: str | None = None, line: int | None = None
    ) -> None:
        """Error."""
        super().__init__(
            "Unable to parse"
            + (f" '{text}'" if text is not None else "")
            + (f" on line {line}" if line is not None else "")
            + f": {message}"
        )


class LengthError(ParseError):
    """Raised when there is a problem with parsing."""

    def __init__(self) -> None:
        """Error."""
        super().__init__("Input length error")


class SectionError(ParseError):
    """Raised when there is a problem with parsing."""

    def __init__(self) -> None:
        """Error."""
        super().__init__("Expected number of section does not number of sections found")


class HeaderError(ParseError):
    """Raised when there is a problem with parsing."""

    def __init__(self, text: str, line: int) -> None:
        """Error."""
        super().__init__("Incorrect header", text, line)


class NoMatchFoundError(ParseError):
    """Raised when there is a problem with parsing."""

    def __init__(self, text: str, line: int) -> None:
        """Error."""
        super().__init__("No match found", text, line)


class MissingDelimiterError(ParseError):
    """Raised when there is a problem with parsing."""

    def __init__(self, text: str, line: int) -> None:
        """Error."""
        super().__init__("Missing delimiter", text, line)


def int_processor(match: Match[str]) -> int:
    """Process match object as an int.

    Args:
        match (Match[str]): the regular expression Match

    Returns:
        int: the result
    """
    return int(match[0])


def int_processor_group(group: str | int) -> Callable[[Match[str]], int]:
    """Process match object as a str.

    Args:
        group (str | int): the group name of numvber to match

    Returns:
        Callable[[Match[str]], int]: the result
    """
    return lambda m: int(m.group(group))


def int_tuple_processor(match: Match[str]) -> tuple[int, ...]:
    """Process match object as an int tuple.

    Args:
        match (Match[str]): the regular expression Match[str]

    Returns:
        tuple[int, ...]: the result
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


def str_processor_group(group: str | int) -> Callable[[Match[str]], str]:
    """Process match object as a str.

    Args:
        group (str | int): the group name of numvber to match

    Returns:
        Callable[[Match[str]], str]: the result
    """
    return lambda m: m.group(group)


def str_tuple_processor(match: Match[str]) -> tuple[str, ...]:
    """Process match object as a str tuple.

    Args:
        match (Match[str]): the regular expression Match

    Returns:
        tuple[str, ...]: the result
    """
    return match.groups()


def str_pair_processor(match: Match[str]) -> tuple[str, str]:
    """Process match object as a str tuple.

    Args:
        match (Match[str]): the regular expression Match

    Returns:
        tuple[str, str]: the result
    """
    return (match[1], match[2])


def dataclass_processor(
    cls: type[T],
) -> Callable[[Match[str]], T]:
    """Create a match processor to process match object as a data class.

    Args:
        cls (type[T]): the data class to initialise

    Returns:
        Callable[[Match[str]], T]: the match processor

    Raises:
        TypeError: if cls is not a DataClass (needed due to mypy typing bug)
    """
    if not is_dataclass(cls):
        raise TypeError  # pragma: no cover

    fields_dict = {f.name: f for f in fields(cls) if f.init}
    return lambda m: cls(
        **{
            k: fields_dict[k].type(v)
            for k, v in m.groupdict().items()
            if k in fields_dict and v is not None
        }
    )


def enum_processor(
    enum: type[T],
) -> Callable[[Match[str]], T]:
    """Create a match processor to process match object as a data class.

    Args:
        enum (type[T]): the enum to initialise

    Raises:
        ValueError: if T is not a subclass of Enum

    Returns:
        Callable[[Match[str]], T]: the match processor
    """
    if any(cls == Enum for cls in enum.__bases__):
        return lambda m: enum(m[0])  # type: ignore [call-arg]
    raise TypeError


def enum_re(enumeration: type[Enum]) -> str:
    """Syntactic sugar for using Enum's in regular expressions.

    Args:
        enumeration (type[Enum]): the enum to use

    Returns:
        str: list of values in the enum, delimited by a "|"
    """
    return "|".join(
        sorted([escape(str(x.value)) for x in enumeration], key=len, reverse=True)
    )


def _validate_input_and_header(
    puzzle_input: list[str],
    min_length: int,
    max_length: int,
    header: tuple[str, ...],
) -> int:
    """Validates the input.

    Args:
        puzzle_input (list[str]): the puzzle input
        min_length (int): the minimum allowable length
        max_length (int): the maximum allowable length
        header (tuple[str, ...], optional): header to validate. Default ()

    Raises:
        ParseError: raised on invalid puzzle_input

    Returns:
        int: the start line of the data, after the header
    """
    # validate puzzle_input
    if puzzle_input is None or not (min_length <= len(puzzle_input) <= max_length):
        raise LengthError

    # validate the optional header
    start = 0
    while start < len(header):
        if not fullmatch(header[start], puzzle_input[start]):
            raise HeaderError(puzzle_input[start], start + 1)

        start += 1

    return start


def parse_lines(
    puzzle_input: list[str],
    *args: tuple[str, Callable[[Match[str]], T]],
    min_length: int = 1,
    max_length: int = maxsize,
    header: tuple[str, ...] = (),
) -> list[T]:
    """Load lines from the parsed patterns.

    Args:
        puzzle_input (list[str]): the puzzle input
        *args (tuple[str, Callable[[Match[str]], T]]): processors called for each match
        min_length (int): the minimum number of lines expected
        max_length (int): the maximum number of lines expected
        header (tuple[str, ...]): header to validate. Default ()

    Raises:
        ParseError: if the puzzle_input has the wrong length

    Returns:
        list[T]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # parse the input
    output: list[T] = []
    for i, line in enumerate(puzzle_input[start:]):
        found = False
        for pattern, match_processor in args:
            if m := fullmatch(pattern, line):
                output.append(match_processor(m))
                found = True
                break
        if not found:
            raise NoMatchFoundError(line, i + 1)
    return output


def parse_single_line(
    puzzle_input: list[str],
    pattern: str,
    match_processor: (Callable[[Match[str]], T]),
) -> T:
    """Load lines from the parsed patterns.

    Args:
        puzzle_input (list[str]): the puzzle input
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
    puzzle_input: list[str],
    *args: tuple[str, Callable[[Match[str]], T]],
    delimiter: str = "",
    require_delimiter: bool = True,
    min_length: int = 1,
    max_length: int = maxsize,
    header: tuple[str, ...] = (),
) -> list[list[T]]:
    """Load lines using the tokenised methods.

    Args:
        puzzle_input (list[str]): the puzzle input
        *args (tuple[str, Callable[[Match[str]], T]]): processors called for each match
        delimiter (str): the delimiter expected between tokens. Defaults to "".
        require_delimiter (bool): delimiter must be present when True. Defaults to True.
        min_length (int): the minimum number of lines expected. Defaults to 1.
        max_length (int): the maximum number of lines expected. Defaults to maxsize.
        header (tuple[str, ...]): header to validate. Defaults to ().

    Raises:
        ParseError: if the input has an invalid pattern and delimiter combination

    Returns:
        list[list[T]]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # parse the input
    output: list[list[T]] = []
    for i, line in enumerate(puzzle_input[start:]):
        # check for at least one delimiter on the line
        if line == "" or (require_delimiter and not search(delimiter, line)):
            raise MissingDelimiterError(line, i + 1)

        # parse each token on the line
        output.append([])
        if delimiter == "":
            tokens = list(line)
        else:
            tokens = [x for x in split(delimiter, line) if x != ""]
        for token in tokens:
            # search for a matching pattern
            found = False
            for pattern, match_processor in args:
                if m := fullmatch(pattern, token):
                    output[-1].append(match_processor(m))
                    found = True
                    break
            if not found:
                raise NoMatchFoundError(line, i + 1)

    return output


def parse_tokens_single_line(
    puzzle_input: list[str],
    *args: tuple[str, Callable[[Match[str]], T]],
    delimiter: str = "",
    require_delimiter: bool = True,
    header: tuple[str, ...] = (),
) -> list[T]:
    """Load lines using the tokenised methods.

    Args:
        puzzle_input (list[str]): the puzzle input
        *args (tuple[str, Callable[[Match[str]], T]]): processors called for each match
        delimiter (str): the delimiter expected between tokens. Defaults to "".
        require_delimiter (bool): when false, the delimiter is optional in the input
        header (tuple[str, ...]): header to validate. Defaults to ().

    Returns:
        list[T]: the parsed output
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
    puzzle_input: list[str],
    pattern: str,
    match_processor: Callable[[Match[str]], T],
    min_length: int = 1,
    max_length: int = maxsize,
    header: tuple[str, ...] = (),
) -> dict[tuple[int, int], T]:
    """Load lines as an x y grid and initialise classes with the whole pattern match.

    Args:
        puzzle_input (list[str]): the puzzle input
        pattern (str): the regular expression pattern for each line
        match_processor (Callable[[Match[str]], T]): processor called for the match
        min_length (int): the minimum number of lines expected
        max_length (int): the maximum number of lines expected
        header (tuple[str, ...]): header to validate. Default ()

    Raises:
        ParseError: if the puzzle_input has the wrong length

    Returns:
        dict[tuple[int, int], T]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # parse the input
    output: dict[tuple[int, int], T] = {}
    for y, line in enumerate(puzzle_input[start:]):
        for x, char in enumerate(line):
            if m := fullmatch(pattern, char):
                output[(x, y)] = match_processor(m)
            else:
                raise NoMatchFoundError(line, y + 1)
    if not output:
        raise NoMatchFoundError("", 1)
    return output


def split_sections(
    puzzle_input: list[str],
    section_break: str = "",
    expected_sections: int = maxsize,
    min_length: int = 1,
    max_length: int = maxsize,
    header: tuple[str, ...] = (),
) -> list[list[str]]:
    """Split the input into sections where a lines matches the section_break regex.

    Args:
        puzzle_input (list[str]): the puzzle input
        section_break (str): the section break regex
        expected_sections (int): the number of sections to expect.
        min_length (int): the minimum number of lines expected
        max_length (int): the maximum number of lines expected
        header (tuple[str, ...]): header to validate. Default ()

    Raises:
        ParseError: if the puzzle_input has incorrect length or number of sections

    Returns:
        list[list[str]]: the parsed output
    """
    start = _validate_input_and_header(puzzle_input, min_length, max_length, header)

    # parse the input into sections
    output: list[list[str]] = []
    section: list[str] = []
    for line in puzzle_input[start:]:
        if fullmatch(section_break, line):
            if section:
                output.append(section)
                section = []
        else:
            section.append(line)
    output.append(section)

    if not output or (expected_sections < maxsize and len(output) != expected_sections):
        raise SectionError

    return output
