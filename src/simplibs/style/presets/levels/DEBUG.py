# Outers
from ..attributes import DIM


DEBUG = DIM
"""Style for debug messages: dimmed text.

Style:
    An alias of `DIM` (code 2).

Example:
    print(DEBUG("cache miss for key 42"))
    # Writes the message in a fainter shade.

Note:
    The same object as `DIM`, under the name that says what it is for.
"""
