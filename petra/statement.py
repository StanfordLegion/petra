"""
This file defines Petra statements.
"""

import re

from abc import ABC, abstractmethod
from llvmlite import ir
from typing import Tuple, Union

from .codegen import CodegenContext
from .expr import Expr, Var
from .symbol import Symbol
from .type import Type
from .typecheck import TypeContext, TypeCheckError
from .validate import ValidateError

#
# Statement
#


class Statement(ABC):
    """
    A Petra statement. Petra functions are composed of statements.
    """

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the statement.

        This performs structural checks on the validity of an statement. It does not
        perform semantics checks.

        """
        pass

    @abstractmethod
    def typecheck(self, ctx: TypeContext) -> None:
        """
        Type check the expression.

        This performs semantic checks on the validity of an statement.

        """
        pass

    @abstractmethod
    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        """
        Code generate the statement.

        Produces LLVM code to evaluate the statment.
        """
        pass


#
# Assign
#


class DefineVar(Statement):
    """
    Defines a new variable.
    """

    def __init__(self, symbol: Symbol, value: Expr):
        self.symbol = symbol
        self.value = value
        self.validate()

    def validate(self) -> None:
        self.symbol.validate()
        self.value.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.value.typecheck(ctx)

        if self.symbol in ctx.variables:
            raise TypeCheckError("Variable '%s' declared multiple times" % self.symbol)
        ctx.variables.add(self.symbol)

        expected_type = self.value.get_type()
        if self.symbol.get_type() != expected_type:
            raise TypeCheckError(
                "Cannot assign expression of type %s to variable '%s' of"
                "type %s" % (expected_type, self.symbol, self.symbol.get_type())
            )

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        value = self.value.codegen(builder, ctx)
        ctx.vars[self.symbol] = builder.alloca(
            self.symbol.get_type().llvm_type(), name=self.symbol.unique_name()
        )
        builder.store(value, ctx.vars[self.symbol])


#
# Assign
#


class Assign(Statement):
    """
    Assigns an expression into a variable.
    """

    def __init__(self, var: Var, value: Expr):
        self.var = var
        self.value = value
        self.validate()

    def validate(self) -> None:
        self.var.validate()
        self.value.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.var.typecheck(ctx)
        self.value.typecheck(ctx)
        expected_type = self.value.get_type()
        if self.var.get_type() != expected_type:
            raise TypeCheckError(
                "Cannot assign expression of type %s to variable '%s' of"
                "type %s" % (expected_type, self.var.symbol, self.var.get_type())
            )

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        value = self.value.codegen(builder, ctx)
        builder.store(value, ctx.vars[self.var.symbol])


#
# Return
#


class Return(Statement):
    """
    Returns the given expression and ends function execution.
    """

    def __init__(self, e: Union[Tuple[()], Expr]):
        self.e = e
        self.validate()

    def validate(self) -> None:
        if isinstance(self.e, Expr):
            self.e.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        if isinstance(self.e, Expr):
            if ctx.return_type == ():
                raise TypeCheckError(
                    "Void functions' return statements must return literal ()."
                )
            else:
                self.e.typecheck(ctx)
                if self.e.get_type() != ctx.return_type:
                    raise TypeCheckError(
                        "Return type %s does not match function declaration."
                        % str(self.e.get_type())
                    )
        else:
            if ctx.return_type != ():
                raise TypeCheckError("Non-void functions cannot return ().")

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        if isinstance(self.e, Expr):
            value = self.e.codegen(builder, ctx)
            builder.ret(value)
        else:
            builder.ret_void()
