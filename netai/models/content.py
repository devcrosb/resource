"""Utilities for extracting values between paired delimiters."""

from __future__ import annotations

import re
from collections.abc import Iterator


def _xml_opening_pattern(delim1: str, delim2: str) -> re.Pattern[str] | None:
    """Return a parameter-tolerant opener when the delimiters are XML tags."""
    opening = re.fullmatch(r"<([A-Za-z_][\w.:-]*)>", delim1)
    closing = re.fullmatch(r"</([A-Za-z_][\w.:-]*)>", delim2)
    if opening is None or closing is None or opening.group(1) != closing.group(1):
        return None

    tag = re.escape(opening.group(1))
    # Quoted attribute values may contain ">", so handle them separately from
    # the other characters in the tag.
    attributes = r"""(?:[^<>"']|"[^"]*"|'[^']*')*"""
    return re.compile(rf"<{tag}\b{attributes}(?<!/)>")


def _tokens(
    text: str,
    delim1: str,
    delim2: str,
) -> Iterator[tuple[int, int, bool]]:
    """Yield delimiter positions as (start, end, is_opening)."""
    opening_pattern = _xml_opening_pattern(delim1, delim2)
    if opening_pattern is not None:
        pattern = re.compile(
            rf"(?P<open>{opening_pattern.pattern})|(?P<close>{re.escape(delim2)})"
        )
        for match in pattern.finditer(text):
            yield match.start(), match.end(), match.lastgroup == "open"
        return

    pattern = re.compile(
        rf"(?P<open>{re.escape(delim1)})|(?P<close>{re.escape(delim2)})"
    )
    for match in pattern.finditer(text):
        yield match.start(), match.end(), match.lastgroup == "open"


def ExtractVals(text: str, delim1: str, delim2: str) -> list[str]:
    """Extract non-blank values inside the innermost paired delimiters.

    ``delim1`` and ``delim2`` must be distinct, non-empty strings. Unmatched
    delimiters are ignored. When XML-style delimiters such as ``<a>`` and
    ``</a>`` are used, attributes on opening tags are accepted.

    The extracted text is returned unchanged; whitespace is only used to
    determine whether a value is empty.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(delim1, str) or not isinstance(delim2, str):
        raise TypeError("delimiters must be strings")
    if not delim1 or not delim2:
        raise ValueError("delimiters must not be empty")
    if delim1 == delim2:
        raise ValueError("start and end delimiters must be distinct")

    # Each frame stores the content start and whether it contains another
    # delimiter pair. Only frames without nested pairs produce results.
    stack: list[tuple[int, bool]] = []
    results: list[str] = []

    for start, end, is_opening in _tokens(text, delim1, delim2):
        if is_opening:
            if stack:
                content_start, _ = stack[-1]
                stack[-1] = (content_start, True)
            stack.append((end, False))
        elif stack:
            content_start, contains_nested = stack.pop()
            if not contains_nested:
                value = text[content_start:start]
                if value.strip():
                    results.append(value)

    return results


__all__ = ["ExtractVals"]
