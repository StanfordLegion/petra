"""
This file defines Petra arithmetic.
"""

from llvmlite import ir
from typing import Optional

from .codegen import CodegenContext
from .expr import Expr
from .type import Int8_t, Int16_t, Int32_t, Int64_t, Type
from .typecheck import TypeContext, TypeCheckError


class ArithmeticBinop(Expr):
    """
    A Petra binary operation of two arithmetic expressions.
    """

    def __init__(self, left: Expr, right: Expr, op: str):
        self.left = left
        self.right = right
        self.op = op
        self.t: Optional[Type] = None
        self.validate()

    def get_type(self) -> Type:
        if isinstance(self.t, Type):
            return self.t
        raise Exception("Expected type to exist - was typecheck called?")

    def validate(self) -> None:
        self.left.validate()
        self.right.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.left.typecheck(ctx)
        t_left = self.left.get_type()
        self.right.typecheck(ctx)
        t_right = self.right.get_type()
        if (t_left, t_right) == (Int8_t, Int8_t):
            self.t = Int8_t
        elif (t_left, t_right) == (Int16_t, Int16_t):
            self.t = Int16_t
        elif (t_left, t_right) == (Int32_t, Int32_t):
            self.t = Int32_t
        elif (t_left, t_right) == (Int64_t, Int64_t):
            self.t = Int64_t
        else:
            raise TypeCheckError(
                "Incompatible types for arithmetic binary operation: %s and %s"
                % (str(t_left), str(t_right))
            )

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        left = self.left.codegen(builder, ctx)
        right = self.right.codegen(builder, ctx)
        # FIXME: figure out a way to be able to type check this
        return getattr(builder, self.op)(left, right)  # type: ignore


class Add(ArithmeticBinop):
    """
    Addition operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "add")


class Sub(ArithmeticBinop):
    """
    Subtraction operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "sub")


class Mul(ArithmeticBinop):
    """
    Multiplication operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "mul")


class Div(ArithmeticBinop):
    """
    Division operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "sdiv")


class Mod(ArithmeticBinop):
    """
    Modulus operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "srem")
