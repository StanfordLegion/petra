"""
This file defines Petra comparisons and boolean logic.
"""

from llvmlite import ir  # type:ignore
from typing import Optional

from .codegen import codegen_expression, convert_type, CodegenContext
from .expr import Expr
from .staticcheck import staticcheck
from .type import Bool_t, Int8_t, Int32_t, Type
from .typecheck import typecheck, TypeContext, TypeException

#
# Comparison
#


class Comparison(Expr):
    """
    A Petra comparison between two arithmetic expressions.
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


@staticcheck.register(Comparison)
def _staticcheck_comparison(c: Comparison) -> None:
    staticcheck(c.left)
    staticcheck(c.right)


@typecheck.register(Comparison)
def _typecheck_comparison(c: Comparison, ctx: TypeContext) -> None:
    typecheck(c.left, ctx)
    t_left = c.left.get_type()
    typecheck(c.right, ctx)
    t_right = c.right.get_type()
    if (t_left, t_right) in ((Int8_t, Int8_t), (Int32_t, Int32_t)):
        c.t = Bool_t
    else:
        raise TypeException(
            "Incompatible types for arithmetic comparison: %s and %s"
            % (str(t_left), str(t_right))
        )


class Lt(Comparison):
    """
    A Petra less-than comparison.
    """

    pass


@codegen_expression.register(Lt)
def _codegen_expression_less_than(
    c: Lt, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    left = codegen_expression(c.left, builder, ctx)
    right = codegen_expression(c.right, builder, ctx)
    return builder.icmp_signed("<", left, right)


class Lte(Comparison):
    """
    A Petra less-than-or-equal comparison.
    """

    pass


@codegen_expression.register(Lte)
def _codegen_expression_less_than_or_equal(
    c: Lte, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    left = codegen_expression(c.left, builder, ctx)
    right = codegen_expression(c.right, builder, ctx)
    return builder.icmp_signed("<=", left, right)


class Gt(Comparison):
    """
    A Petra greater-than comparison.
    """

    pass


@codegen_expression.register(Gt)
def _codegen_expression_greater_than(
    c: Gt, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    left = codegen_expression(c.left, builder, ctx)
    right = codegen_expression(c.right, builder, ctx)
    return builder.icmp_signed(">", left, right)


class Gte(Comparison):
    """
    A Petra greater-than-or-equal comparison.
    """

    pass


@codegen_expression.register(Gte)
def _codegen_expression_greater_than_or_equal(
    c: Gte, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    left = codegen_expression(c.left, builder, ctx)
    right = codegen_expression(c.right, builder, ctx)
    return builder.icmp_signed(">=", left, right)


#
# EqualityComparison
#


class EqualityComparison(Comparison):
    """
    A Petra equality comparison between two expressions.
    """

    pass


@typecheck.register(EqualityComparison)
def _typecheck_equality_comparison(c: EqualityComparison, ctx: TypeContext) -> None:
    typecheck(c.left, ctx)
    t_left = c.left.get_type()
    typecheck(c.right, ctx)
    t_right = c.right.get_type()
    if (t_left, t_right) in ((Bool_t, Bool_t), (Int8_t, Int8_t), (Int32_t, Int32_t)):
        c.t = Bool_t
    else:
        raise TypeException(
            "Incompatible types for equality comparison: %s and %s"
            % (str(t_left), str(t_right))
        )


class Eq(EqualityComparison):
    """
    A Petra equal comparison.
    """

    pass


@codegen_expression.register(Eq)
def _codegen_expression_equal(
    c: Eq, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    left = codegen_expression(c.left, builder, ctx)
    right = codegen_expression(c.right, builder, ctx)
    return builder.icmp_signed("==", left, right)


class Neq(EqualityComparison):
    """
    A Petra unequal comparison.
    """

    pass


@codegen_expression.register(Neq)
def _codegen_expression_not_equal(
    c: Neq, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    left = codegen_expression(c.left, builder, ctx)
    right = codegen_expression(c.right, builder, ctx)
    return builder.icmp_signed("!=", left, right)


#
# BooleanBinop
#


class BooleanBinop(Expr):
    """
    A Petra binary operation of two boolean expressions.
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


@staticcheck.register(BooleanBinop)
def _staticcheck_boolean_binop(b: BooleanBinop) -> None:
    staticcheck(b.left)
    staticcheck(b.right)


@typecheck.register(BooleanBinop)
def _typecheck_boolean_binop(b: BooleanBinop, ctx: TypeContext) -> None:
    typecheck(b.left, ctx)
    t_left = b.left.get_type()
    typecheck(b.right, ctx)
    t_right = b.right.get_type()
    if (t_left, t_right) == (Bool_t, Bool_t):
        b.t = Bool_t
    else:
        raise TypeException(
            "Incompatible types for boolean binary operation: %s and %s"
            % (str(t_left), str(t_right))
        )


class And(BooleanBinop):
    """
    A Petra boolean and operation.
    """

    pass


@codegen_expression.register(And)
def _codegen_expression_and(
    b: And, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    left = codegen_expression(b.left, builder, ctx)
    temp = builder.alloca(convert_type(Bool_t))
    builder.store(left, temp)
    with builder.if_then(left):
        right = codegen_expression(b.right, builder, ctx)
        builder.store(right, temp)
    return builder.load(temp)


class Or(BooleanBinop):
    """
    A Petra boolean or operation.
    """

    pass


@codegen_expression.register(Or)
def _codegen_expression_or(
    b: Or, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    left = codegen_expression(b.left, builder, ctx)
    temp = builder.alloca(convert_type(Bool_t))
    builder.store(left, temp)
    notleft = builder.sub(ir.Constant(convert_type(Bool_t), True), left)
    with builder.if_then(notleft):
        right = codegen_expression(b.right, builder, ctx)
        builder.store(right, temp)
    return builder.load(temp)


#
# Not
#


class Not(Expr):
    """
    A Petra boolean not operation.
    """

    def __init__(self, e: Expr):
        self.e = e
        self.t: Optional[Type] = None
        staticcheck(self)

    def get_type(self) -> Type:
        if isinstance(self.t, Type):
            return self.t
        raise Exception("Expected type to exist - was typecheck called?")


@staticcheck.register(Not)
def _staticcheck_not(b: Not) -> None:
    staticcheck(b.e)


@typecheck.register(Not)
def _typecheck_not(b: Not, ctx: TypeContext) -> None:
    typecheck(b.e, ctx)
    t = b.e.get_type()
    if t == Bool_t:
        b.t = Bool_t
    else:
        raise TypeException("Incompatible type for boolean not:: %s" % (str(t)))


@codegen_expression.register(Not)
def _codegen_expression_not(
    b: Not, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    value = codegen_expression(b.e, builder, ctx)
    return builder.sub(ir.Constant(convert_type(Bool_t), True), value)
