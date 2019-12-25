"""
This file defines Petra arithmetic.
"""

from llvmlite import ir # type:ignore
from typing import Optional

from .codegen import codegen_expression, CodegenContext
from .expr import Expr
from .staticcheck import staticcheck
from .type import Int8_t, Int32_t, Type
from .typecheck import typecheck, TypeContext, TypeException

class ArithmeticBinop(Expr):
    """
    A Petra binary operation of two arithmetic expressions.
    """
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right
        self.t: Optional[Type] = None
        staticcheck(self)

    def get_type(self) -> Type:
        if isinstance(self.t, Type):
            return self.t
        raise Exception("Expected type to exist - was typecheck called?")

@staticcheck.register(ArithmeticBinop)
def _staticcheck_arithmetic_binop(b: ArithmeticBinop) -> None:
    staticcheck(b.left)
    staticcheck(b.right)

@typecheck.register(ArithmeticBinop)
def _typecheck_arithmetic_binop(b: ArithmeticBinop, ctx: TypeContext) -> None:
    typecheck(b.left, ctx)
    t_left = b.left.get_type()
    typecheck(b.right, ctx)
    t_right = b.right.get_type()
    if (t_left, t_right) == (Int8_t, Int8_t):
        b.t = Int8_t
    elif (t_left, t_right) == (Int32_t, Int32_t):
        b.t = Int32_t
    else:
        raise TypeException("Incompatible types for arithmetic binary operation: %s and %s"
                %(str(t_left), str(t_right)))

class Add(ArithmeticBinop):
    """
    A Petra addition.
    """
    pass

@codegen_expression.register(Add)
def _codegen_expression_add(a: Add, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    left = codegen_expression(a.left, builder, ctx)
    right = codegen_expression(a.right, builder, ctx)
    return builder.add(left, right)

class Sub(ArithmeticBinop):
    """
    A Petra subtraction.
    """
    pass

@codegen_expression.register(Sub)
def _codegen_expression_sub(a: Sub, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    left = codegen_expression(a.left, builder, ctx)
    right = codegen_expression(a.right, builder, ctx)
    return builder.sub(left, right)

class Mul(ArithmeticBinop):
    """
    A Petra multiplication.
    """
    pass

@codegen_expression.register(Mul)
def _codegen_expression_mul(a: Mul, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    left = codegen_expression(a.left, builder, ctx)
    right = codegen_expression(a.right, builder, ctx)
    return builder.mul(left, right)

class Div(ArithmeticBinop):
    """
    A Petra division.
    """
    pass

@codegen_expression.register(Div)
def _codegen_expression_div(a: Div, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    left = codegen_expression(a.left, builder, ctx)
    right = codegen_expression(a.right, builder, ctx)
    return builder.sdiv(left, right)

class Mod(ArithmeticBinop):
    """
    A Petra mod operation.
    """
    pass

@codegen_expression.register(Mod)
def _codegen_expression_mod(a: Mod, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> ir.Value:
    left = codegen_expression(a.left, builder, ctx)
    right = codegen_expression(a.right, builder, ctx)
    return builder.srem(left, right)
