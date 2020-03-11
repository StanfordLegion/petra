"""
This file defines the type context and errors.
"""

from __future__ import annotations

from typing import Dict, Tuple

from .type import Ftypein, Ftypeout, Type


class TypeContext(object):
    """
    A typing context for use in typechecking.
    """

    def __init__(
        self, functypes: Dict[str, Tuple[Ftypein, Ftypeout]], return_type: Ftypeout
    ):
        self.types: Dict[str, Type] = dict()
        self.functypes = functypes
        self.return_type = return_type

    def copy(self) -> TypeContext:
        ctx_copy = TypeContext(dict(self.functypes), self.return_type)
        ctx_copy.types = dict(self.types)
        return ctx_copy


class TypeCheckError(Exception):
    pass
