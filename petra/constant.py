"""
This file defines Petra constants.
"""

from llvmlite import ir # type:ignore

from .codegen import codegen_expression, convert_type, CodegenContext
from .expr import Expr
from .staticcheck import staticcheck, StaticException
from .type import Bool_t, Float_t, Int8_t, Int32_t, Type
from .typecheck import typecheck, TypeContext

#
# Bool
#

class Bool(Expr):
    """
    A Petra boolean constant.
    """
    def __init__(self, value: bool):
        self.value = value
        self.t = Bool_t
        staticcheck(self)

    def get_type(self) -> Type:
        return self.t

@staticcheck.register(Bool)
def _staticcheck_bool(b: Bool) -> None:
    # If it satisfies the type hints, it must be statically sound.
    pass

@typecheck.register(Bool)
def _typecheck_bool(b: Bool, ctx: TypeContext) -> None:
    # By construction, this must typecheck.
    pass

@codegen_expression.register(Bool)
def _codegen_expression_bool(b: Bool, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    return ir.Constant(convert_type(b.get_type()), b.value)

#
# Float
#

class Float(Expr):
    """
    A Petra single-precision floating point constant.
    """
    def __init__(self, value: float):
        self.value = value
        self.t = Float_t
        staticcheck(self)

    def get_type(self) -> Type:
        return self.t

@staticcheck.register(Float)
def _staticcheck_float(f: Float) -> None:
    # Technically, ir.Constant allows any Python float.
    # TODO: check what the practical bounds are
    pass

@typecheck.register(Float)
def _typecheck_float(f: Float, ctx: TypeContext) -> None:
    # By construction, this must typecheck.
    pass

@codegen_expression.register(Float)
def _codegen_expression_float(f: Float, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    return ir.Constant(convert_type(f.get_type()), f.value)

#
# Int8
#

class Int8(Expr):
    """
    A Petra 8-bit integer constant.
    """
    def __init__(self, value: int):
        self.value = value
        self.t = Int8_t
        staticcheck(self)

    def get_type(self) -> Type:
        return self.t

@staticcheck.register(Int8)
def _staticcheck_int8(i: Int8) -> None:
    if not (-128 <= i.value < 128):
        raise StaticException("Int8 value not in the range [-128, 128).")

@typecheck.register(Int8)
def _typecheck_int8(i: Int8, ctx: TypeContext) -> None:
    # By construction, this must typecheck.
    pass

@codegen_expression.register(Int8)
def _codegen_expression_int8(i : Int8, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    return ir.Constant(convert_type(i.get_type()), i.value)

#
# Int32
#

class Int32(Expr):
    """
    A Petra 32-bit integer constant.
    """
    def __init__(self, value: int):
        self.value = value
        self.t = Int32_t
        staticcheck(self)

    def get_type(self) -> Type:
        return self.t

@staticcheck.register(Int32)
def _staticcheck_int32(i: Int32) -> None:
    if not (-(2**31) <= i.value < (2**31)):
        raise StaticException("Int32 value not in the range [-2**31, 2**31).")

@typecheck.register(Int32)
def _typecheck_int32(i: Int32, ctx: TypeContext) -> None:
    # By construction, this must typecheck.
    pass

@codegen_expression.register(Int32)
def _codegen_expression_int32(i: Int32, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    return ir.Constant(convert_type(i.get_type()), i.value)
