"""
This file defines the top-level staticcheck() function.
"""

from functools import singledispatch


@singledispatch
def staticcheck(syntax) -> None:
    """
    Check properties about syntax that can be checked statically.
    """
    raise NotImplementedError("Unsupported type: " + str(type(syntax)))


class StaticException(Exception):
    pass
