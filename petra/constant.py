"""
This file defines Petra constants.
"""

from llvmlite import ir  # type:ignore

from .codegen import convert_type, CodegenContext
from .expr import Expr
from .validate import ValidateError
from .type import Bool_t, Float_t, Int8_t, Int32_t, Type
from .typecheck import TypeContext

#
# Bool
#


class Bool(Expr):
    """
    Boolean constant.
    """

    def __init__(self, value: bool):
        self.value = value
        self.t = Bool_t
        self.validate()

    def get_type(self) -> Type:
        return self.t

    def validate(self) -> None:
        # If it satisfies the type hints, it must be statically sound.
        pass

    def typecheck(self, ctx: TypeContext) -> None:
        # By construction, this must typecheck.
        pass

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        return ir.Constant(convert_type(self.get_type()), self.value)


#
# Float
#


class Float(Expr):
    """
    A single-precision floating point constant.
    """

    def __init__(self, value: float):
        self.value = value
        self.t = Float_t
        self.validate()

    def get_type(self) -> Type:
        return self.t

    def validate(self) -> None:
        # Technically, ir.Constant allows any Python float.
        # TODO: check what the practical bounds are
        pass

    def typecheck(self, ctx: TypeContext) -> None:
        # By construction, this must typecheck.
        pass

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        return ir.Constant(convert_type(self.get_type()), self.value)


#
# Int8
#


class Int8(Expr):
    """
    An 8-bit integer constant.
    """

    def __init__(self, value: int):
        self.value = value
        self.t = Int8_t
        self.validate()

    def get_type(self) -> Type:
        return self.t

    def validate(self) -> None:
        if not (-128 <= self.value < 128):
            raise ValidateError("Int8 value not in the range [-128, 128).")

    def typecheck(self, ctx: TypeContext) -> None:
        # By construction, this must typecheck.
        pass

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        return ir.Constant(convert_type(self.get_type()), self.value)


#
# Int32
#


class Int32(Expr):
    """
    A 32-bit integer constant.
    """

    def __init__(self, value: int):
        self.value = value
        self.t = Int32_t
        self.validate()

    def get_type(self) -> Type:
        return self.t

    def validate(self) -> None:
        if not (-(2 ** 31) <= self.value < (2 ** 31)):
            raise ValidateError("Int32 value not in the range [-2**31, 2**31).")

    def typecheck(self, ctx: TypeContext) -> None:
        # By construction, this must typecheck.
        pass

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        return ir.Constant(convert_type(self.get_type()), self.value)
