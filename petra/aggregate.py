"""
This file defines methods for setting and accessing elements for StructType and ArrayType
"""

import re

from abc import ABC, abstractmethod
from llvmlite import ir
from typing import Optional, Dict

from .codegen import CodegenContext
from .validate import ValidateError
from .symbol import Symbol
from .expr import Expr, Var
from .type import Type, StructType, Int32_t, ArrayType
from .typecheck import TypeContext, TypeCheckError


class GetElement(Expr):
    """
    Get element of an array by index or get field of a struct using the index/name of the field
    Returns the element at given index/name
    """

    def __init__(
        self, struct: Expr, idx: Optional[int] = None, name: Optional[str] = None
    ):
        self.struct = struct
        self.idx = idx
        self.name = name
        self.validate()

    def get_type(self) -> Type:
        t_struct = self.struct.get_type()
        if isinstance(t_struct, StructType):
            assert self.idx is not None
            return t_struct.elements[self.idx]
        elif isinstance(t_struct, ArrayType):
            return t_struct.element
        else:
            assert False

    def validate(self) -> None:
        assert self.idx is not None or self.name is not None

    def typecheck(self, ctx: TypeContext) -> None:
        t_struct = self.struct.get_type()
        if not (isinstance(t_struct, StructType) or isinstance(t_struct, ArrayType)):
            raise TypeCheckError(
                "%s is not an Aggregate Type (StructType or ArrayType)" % str(t_struct)
            )
        if isinstance(t_struct, StructType):
            if self.idx is None and self.name is not None:
                self.idx = t_struct.name_to_index[self.name]

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        struct = self.struct.codegen(builder, ctx)
        assert self.idx is not None
        return builder.extract_value(struct, self.idx)


class SetElement(Expr):
    """
    Set element of an array by index or set field of a struct by index/name of the field to a new value
    Returns a new object of type Array or Struct with the element set to the new value
    """

    def __init__(
        self,
        struct: Expr,
        value: Expr,
        idx: Optional[int] = None,
        name: Optional[str] = None,
    ):
        self.struct = struct
        self.idx = idx
        self.name = name
        self.value = value
        self.validate()

    def get_type(self) -> Type:
        t_struct = self.struct.get_type()
        return t_struct

    def validate(self) -> None:
        assert self.idx is not None or self.name is not None

    def typecheck(self, ctx: TypeContext) -> None:
        t_struct = self.struct.get_type()
        if not (isinstance(t_struct, StructType) or isinstance(t_struct, ArrayType)):
            raise TypeCheckError(
                "%s is not an Aggregate Type (StructType or ArrayType)" % str(t_struct)
            )
        if isinstance(t_struct, StructType):
            if self.idx is None and self.name is not None:
                self.idx = t_struct.name_to_index[self.name]

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        struct = self.struct.codegen(builder, ctx)
        value = self.value.codegen(builder, ctx)
        assert self.idx is not None
        return builder.insert_value(struct, value, self.idx)
