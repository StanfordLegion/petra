"""
This file defines Petra statements.
"""

import re

from abc import ABC, abstractmethod
from llvmlite import ir
from typing import Tuple, Union

from .codegen import convert_type, CodegenContext
from .expr import Expr, Var
from .validate import ValidateError
from .type import Type
from .typecheck import TypeContext, TypeCheckError

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

# Declare is an artifact of Assign, and is not a Statement or any kind of core
# object on its own.
class Declare(object):
    """
    Declares a new variable. Only valid as the assignee in an Assign statement
    or when adding a function.
    """

    def __init__(self, t: Type, name: str):
        self.t = t
        self.name = name


class Assign(Statement):
    """
    Assigns an expression into a possibly new variable.
    """

    def __init__(self, var: Union[Declare, Var], e: Expr):
        self.var = var
        self.e = e
        self.validate()

    def validate(self) -> None:
        if isinstance(self.var, Declare):
            if not re.match(r"^[a-z][a-zA-Z0-9_]*$", self.var.name):
                raise ValidateError(
                    "Variable name '%s' does not match regex "
                    "^[a-z][a-zA-Z0-9_]*$" % self.var.name
                )
        else:
            self.var.validate()
        self.e.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.e.typecheck(ctx)
        if isinstance(self.var, Declare):
            if self.var.name in ctx.types:
                raise TypeCheckError("Cannot redeclare variable %s" % self.var.name)
            ctx.types[self.var.name] = self.var.t
        else:
            self.var.typecheck(ctx)
        expected_type = self.e.get_type()
        if ctx.types[self.var.name] != expected_type:
            raise TypeCheckError(
                "Cannot assign expression of type %s to variable of"
                "type %s" % (expected_type, ctx.types[self.var.name])
            )

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        exp = self.e.codegen(builder, ctx)
        if isinstance(self.var, Declare):
            ctx.vars[self.var.name] = builder.alloca(
                convert_type(self.var.t), name=self.var.name
            )
        builder.store(exp, ctx.vars[self.var.name])


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
