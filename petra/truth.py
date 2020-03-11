"""
This file defines Petra comparisons and boolean logic.
"""

from llvmlite import ir
from typing import Optional

from .codegen import convert_type, CodegenContext
from .expr import Expr
from .validate import ValidateError
from .type import Bool_t, Int8_t, Int32_t, Type
from .typecheck import TypeContext, TypeCheckError

#
# Comparison
#


class Comparison(Expr):
    """
    Comparison operator.
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
        if self.op not in ["<", "<=", ">", ">="]:
            raise ValidateError("Invalid operator for comparison: %s" % str(self.op))

    def typecheck(self, ctx: TypeContext) -> None:
        self.left.typecheck(ctx)
        t_left = self.left.get_type()
        self.right.typecheck(ctx)
        t_right = self.right.get_type()
        if (t_left, t_right) in ((Int8_t, Int8_t), (Int32_t, Int32_t)):
            self.t = Bool_t
        else:
            raise TypeCheckError(
                "Incompatible types for arithmetic comparison: %s and %s"
                % (str(t_left), str(t_right))
            )

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        left = self.left.codegen(builder, ctx)
        right = self.right.codegen(builder, ctx)
        return builder.icmp_signed(self.op, left, right)


class Lt(Comparison):
    """
    Less-than operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "<")


class Lte(Comparison):
    """
    Less-than-or-equal operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "<=")


class Gt(Comparison):
    """
    Greater-than operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, ">")


class Gte(Comparison):
    """
    Greater-than-or-equal operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, ">=")


#
# Equality
#


class Equality(Comparison):
    """
    Equality operator.
    """

    def validate(self) -> None:
        self.left.validate()
        self.right.validate()
        if self.op not in ["==", "!="]:
            raise ValidateError("Invalid operator for equality: %s" % str(self.op))

    def typecheck(self, ctx: TypeContext) -> None:
        self.left.typecheck(ctx)
        t_left = self.left.get_type()
        self.right.typecheck(ctx)
        t_right = self.right.get_type()
        if (t_left, t_right) in (
            (Bool_t, Bool_t),
            (Int8_t, Int8_t),
            (Int32_t, Int32_t),
        ):
            self.t = Bool_t
        else:
            raise TypeCheckError(
                "Incompatible types for equality comparison: %s and %s"
                % (str(t_left), str(t_right))
            )


class Eq(Equality):
    """
    Equals operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "==")


class Neq(Equality):
    """
    Not-equals operator.
    """

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "!=")


#
# Logical
#


class Logical(Expr):
    """
    Logical (short-circuiting) boolean operator.
    """

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right
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
        if (t_left, t_right) == (Bool_t, Bool_t):
            self.t = Bool_t
        else:
            raise TypeCheckError(
                "Incompatible types for boolean binary operation: %s and %s"
                % (str(t_left), str(t_right))
            )


class And(Logical):
    """
    Logical (short-circuiting) and operation.
    """

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        left = self.left.codegen(builder, ctx)
        temp = builder.alloca(convert_type(Bool_t))
        builder.store(left, temp)
        with builder.if_then(left):
            right = self.right.codegen(builder, ctx)
            builder.store(right, temp)
        return builder.load(temp)


class Or(Logical):
    """
    Logical (short-circuiting) or operation.
    """

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        left = self.left.codegen(builder, ctx)
        temp = builder.alloca(convert_type(Bool_t))
        builder.store(left, temp)
        notleft = builder.sub(ir.Constant(convert_type(Bool_t), True), left)
        with builder.if_then(notleft):
            right = self.right.codegen(builder, ctx)
            builder.store(right, temp)
        return builder.load(temp)


#
# Not
#


class Not(Expr):
    """
    Logical not operator.
    """

    def __init__(self, e: Expr):
        self.e = e
        self.t: Optional[Type] = None
        self.validate()

    def get_type(self) -> Type:
        if isinstance(self.t, Type):
            return self.t
        raise Exception("Expected type to exist - was typecheck called?")

    def validate(self) -> None:
        self.e.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.e.typecheck(ctx)
        t = self.e.get_type()
        if t == Bool_t:
            self.t = Bool_t
        else:
            raise TypeCheckError("Incompatible type for boolean not:: %s" % (str(t)))

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        value = self.e.codegen(builder, ctx)
        return builder.sub(ir.Constant(convert_type(Bool_t), True), value)
