"""
This file defines Petra symbols.
"""

import re

from .type import Type
from .validate import ValidateError

_next_id = 0


class Symbol(object):
    """
    A symbol.
    """

    def __init__(self, type_: Type, name: str):
        global _next_id
        self.t = type_
        self.name = name
        self.id = _next_id
        _next_id += 1
        self.validate()

    def __str__(self) -> str:
        return self.name

    def get_type(self) -> Type:
        return self.t

    def validate(self) -> None:
        if not re.match(r"^[a-z][a-zA-Z0-9_]*$", self.name):
            raise ValidateError(
                "Variable name '%s' does not match regex "
                "^[a-z][a-zA-Z0-9_]*$" % self.name
            )

    def unique_name(self) -> str:
        return "_%s_%s" % (self.id, self.name)
