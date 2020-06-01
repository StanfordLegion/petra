"""
This file defines Petra types.
"""

from abc import ABC, abstractmethod
from llvmlite import ir
from typing import Generic, Optional, Tuple, TypeVar, Union

from .validate import ValidateError


class Type(object):
    """
    A type.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def llvm_type(self) -> ir.Type:
        """
        Return the LLVM type of the given type.
        """
        assert False, "unimplemented"


_T = TypeVar("_T")


class ValueType(Type, Generic[_T]):
    def validate(self, value: _T) -> None:
        """
        Validate values of the type.
        """
        assert False, "unimplemented"


class IntType(ValueType[int]):
    """
    An integer type.
    """

    def __init__(self, bits: int):
        super().__init__("Int%d_t" % bits)
        self.bits = bits

    def validate(self, value: int) -> None:
        exp = self.bits - 1
        if not (-(1 << exp) <= value < (1 << exp)):
            raise ValidateError(
                "Int%d_t value not in the range [-2**%d, 2**%d)."
                % (self.bits, exp, exp)
            )

    def llvm_type(self) -> ir.Type:
        return ir.IntType(self.bits)


class FloatType(ValueType[float]):
    """
    An floating point type.
    """

    def __init__(self, bits: int, name: Optional[str] = None):
        if bits not in (32, 64):
            raise ValidateError("Float bits must be 32 or 64")
        super().__init__(name or "Float%d_t" % bits)
        self.bits = bits

    def validate(self, value: float) -> None:
        pass

    def llvm_type(self) -> ir.Type:
        if self.bits == 32:
            return ir.FloatType()
        elif self.bits == 64:
            return ir.DoubleType()
        else:
            assert False


class BoolType(ValueType[bool]):
    """
    An boolean type.
    """

    def __init__(self) -> None:
        super().__init__("Bool_t")

    def validate(self, value: bool) -> None:
        pass

    def llvm_type(self) -> ir.Type:
        return ir.IntType(1)


# Type aliases for functions.
Ftypein = Tuple[Type, ...]
Ftypeout = Union[Tuple[()], Type]

Int8_t = IntType(8)
Int16_t = IntType(16)
Int32_t = IntType(32)
Int64_t = IntType(64)

Float32_t = FloatType(32)
Float64_t = FloatType(64)

Bool_t = BoolType()
