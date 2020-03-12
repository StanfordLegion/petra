"""
This file defines the type context and errors.
"""

from __future__ import annotations

from typing import Dict, Set, Tuple

from .symbol import Symbol
from .type import Ftypein, Ftypeout, Type


class TypeContext(object):
    """
    A typing context for use in typechecking.
    """

    def __init__(
        self, functypes: Dict[str, Tuple[Ftypein, Ftypeout]], return_type: Ftypeout
    ):
        self.variables: Set[Symbol] = set()
        self.functypes = functypes
        self.return_type = return_type

    def copy(self) -> TypeContext:
        ctx_copy = TypeContext(dict(self.functypes), self.return_type)
        ctx_copy.variables = set(self.variables)
        return ctx_copy


class TypeCheckError(Exception):
    pass
