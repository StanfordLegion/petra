"""
This file defines the top-level validate() function.
"""

from functools import singledispatch


@singledispatch
def validate(syntax) -> None:
    """
    Check properties about syntax that can be checked statically.
    """
    raise NotImplementedError("Unsupported type: " + str(type(syntax)))


class ValidateError(Exception):
    pass
