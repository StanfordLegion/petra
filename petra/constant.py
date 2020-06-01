"""
This file defines Petra constants.
"""

from typing import Generic, TypeVar
from llvmlite import ir

from .codegen import CodegenContext
from .expr import Expr
from .validate import ValidateError
from .type import (
    Bool_t,
    Float32_t,
    Float64_t,
    Int8_t,
    Int16_t,
    Int32_t,
    Int64_t,
    Type,
    ValueType,
)
from .typecheck import TypeContext

#
# Constant
#

_VT = TypeVar("_VT")


class Constant(Expr, Generic[_VT]):
    """
    A constant expression.
    """

    def __init__(self, value: _VT, value_type: ValueType[_VT]):
        self.value = value
        self.t = value_type
        self.validate()

    def get_type(self) -> Type:
        return self.t

    def validate(self) -> None:
        self.t.validate(self.value)

    def typecheck(self, ctx: TypeContext) -> None:
        pass

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        return ir.Constant(self.t.llvm_type(), self.value)


class Int8(Constant[int]):
    """
    An Int8_t constant.
    """

    def __init__(self, value: int):
        super().__init__(value, Int8_t)


class Int16(Constant[int]):
    """
    An Int16_t constant.
    """

    def __init__(self, value: int):
        super().__init__(value, Int16_t)


class Int32(Constant[int]):
    """
    An Int32_t constant.
    """

    def __init__(self, value: int):
        super().__init__(value, Int32_t)


class Int64(Constant[int]):
    """
    An Int64_t constant.
    """

    def __init__(self, value: int):
        super().__init__(value, Int64_t)


class Float32(Constant[float]):
    """
    An Float32_t constant.
    """

    def __init__(self, value: float):
        super().__init__(value, Float32_t)


class Float64(Constant[float]):
    """
    An Float64_t constant.
    """

    def __init__(self, value: float):
        super().__init__(value, Float64_t)


class Bool(Constant[bool]):
    """
    A Bool_t constant.
    """

    def __init__(self, value: bool):
        super().__init__(value, Bool_t)
