"""
This file defines Petra types.
"""

from typing import Tuple, Union


class Type(object):
    """
    The "type" of Petra types.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name


# Type aliases for functions.
Ftypein = Tuple[Type, ...]
Ftypeout = Union[Tuple[()], Type]

# A Petra 8-bit integer type.
Int8_t = Type("Int8_t")

# A Petra 32-bit integer type.
Int32_t = Type("Int32_t")

# A Petra single-precision float type.
Float_t = Type("Float_t")

# A Petra boolean type.
Bool_t = Type("Bool_t")
