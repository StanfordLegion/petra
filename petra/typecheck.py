"""
This file defines the top-level typecheck() function.
"""

from functools import singledispatch
from typing import Dict, Tuple

from .type import Ftypein, Ftypeout, Type

class TypeContext(object):
    """
    A typing context for use in typechecking.
    """
    def __init__(self, functypes: Dict[str, Tuple[Ftypein, Ftypeout]],
            return_type: Ftypeout):
        self.types: Dict[str, Type] = dict()
        self.functypes = functypes
        self.return_type = return_type
    def copy(self):
        ctx_copy = TypeContext(dict(self.functypes), self.return_type)
        ctx_copy.types = dict(self.types)
        return ctx_copy

@singledispatch
def typecheck(syntax, ctx: TypeContext) -> None:
    """
    Check types for syntax and write a type for expressions.
    """
    raise NotImplementedError("Unsupported type: " + str(type(syntax)))

class TypeException(Exception):
    pass
