"""
This file defines the pointer dereference class.
"""

import re

from abc import ABC, abstractmethod
from llvmlite import ir
from typing import Optional

from .codegen import CodegenContext
from .validate import ValidateError
from .symbol import Symbol
from .expr import Expr, Var
from .type import Type, PointerType
from .typecheck import TypeContext, TypeCheckError


class Deref(Expr):
    def __init__(self, ptr: Expr):
        self.ptr = ptr
        self.validate()

    def get_type(self) -> Type:
        t_ptr = self.ptr.get_type()
        if isinstance(t_ptr, PointerType):
            return t_ptr.pointee
        else:
            assert False

    def validate(self) -> None:
        pass

    def typecheck(self, ctx: TypeContext) -> None:
        t_ptr = self.ptr.get_type()
        if not isinstance(t_ptr, PointerType):
            raise TypeCheckError("%s is not a PointerType" % str(t_ptr))

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        ptr = self.ptr.codegen(builder, ctx)
        return builder.load(ptr)
