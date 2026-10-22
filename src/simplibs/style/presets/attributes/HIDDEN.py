# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


HIDDEN = StyleDefiner(ANSI.HIDDEN)
"""Hidden (concealed) text.

Style:
    Attribute 8 (`\\033[8m`).

Example:
    print(HIDDEN("secret"))
    # Writes the text invisibly.

Note:
    The text is hidden on the screen only — it is still in the output and can be copied. Do not use it to protect secrets.
"""
