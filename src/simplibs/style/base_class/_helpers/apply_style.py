# Outers
from ...constants import ESCAPE_PREFIX, RESET_SEQUENCE
# Inners
from .patterns import RESET_PATTERN


def apply_style(
    sequence: str,
    text: str,
) -> str:
    """Wrap a text in a style sequence and a reset.

    Args:
        sequence: The escape sequence that switches the style on.
        text: The text to style.

    Returns:
        The text between the sequence and the reset. An empty text stays
        empty. A lone reset inside the text (`\\033[0m`, `\\033[00m` or
        `\\033[m`) is followed by the sequence again, so the style continues
        after an inner styled part.
    """

    # 1. There is nothing to style in an empty text
    if not text:
        return text

    # 2. An inner style ends with a reset that would end this style too —
    #    switch this style back on right after every such reset
    if ESCAPE_PREFIX in text:
        text = RESET_PATTERN.sub(lambda match: f"{match.group(0)}{sequence}", text)

    # 3. Wrap the text and end with a reset
    return f"{sequence}{text}{RESET_SEQUENCE}"


_DESIGN_NOTES = """
# apply_style — Styles Inside Styles

## Purpose
`RED("a " + BOLD("b") + " c")` should print " c" in red. Without step 2 the
reset that closes `BOLD("b")` also ends the red, and " c" comes out plain.

## Which Resets Are Recognized
Every spelling of the lone reset: `\\033[0m`, `\\033[00m` and `\\033[m`. The
last two come from other tools (`git diff --color`, `ls --color` and shell
prompts write them), so styling their output works too.

## What Is Not Handled
A reset combined with other codes (`\\033[0;1m`) and a partial reset such as
`\\033[39m` are left alone: what the outer style should become after them is
a guess, and the library does not rewrite sequences it did not write.

## Cheap When There Is Nothing to Restore
Only a text that contains an escape character is searched at all, so plain
text pays for one substring check.

## An Empty Text Stays Empty
`RED("")` would otherwise write two sequences around nothing, which shows up
as noise in logs and in tests that compare output.
"""
