"""
This file defines Petra expressions.
"""

import re

from abc import ABC, abstractmethod
from llvmlite import ir  # type:ignore
from typing import Optional

from .codegen import CodegenContext
from .validate import ValidateError
from .type import Type
from .typecheck import TypeContext, TypeCheckError


class Expr(ABC):
    """
    An expression. Expressions have a type and can be evaluated.
    """

    @abstractmethod
    def get_type(self) -> Type:
        """
        Returns the type of the expression.

        This function can only be called after typecheck() has been called on self.
        """
        pass

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the expression.

        This performs structural checks on the validity of an expression (e.g. an
        arithemtic expression has a valid operator). It does not perform semantics checks.

        """
        pass

    @abstractmethod
    def typecheck(self, ctx: TypeContext) -> None:
        """Type check the expression.

        This performs semantic checks on the validity of an expression (e.g. the right and
        left hand sides of an arithmetic expression are of compatible types). After
        calling this method it is possible to call get_type() to determine the type of the
        expression.
        """
        pass

    @abstractmethod
    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        """Code generate the expression.

        Produces LLVM code to evaluate the expression.
        """
        pass


class Var(Expr):
    """
    A Petra variable. Variables must be introduced in a Declare statement before
    use.
    """

    def __init__(self, name: str):
        self.name = name
        self.t: Optional[Type] = None
        self.validate()

    def get_type(self) -> Type:
        if isinstance(self.t, Type):
            return self.t
        raise Exception("Expected type to exist - was typecheck called?")

    def validate(self) -> None:
        if not re.match(r"^[a-z][a-zA-Z0-9_]*$", self.name):
            raise ValidateError(
                "Variable name '%s' does not match regex "
                "^[a-z][a-zA-Z0-9_]*$" % self.name
            )

    def typecheck(self, ctx: TypeContext) -> None:
        if self.name not in ctx.types:
            raise TypeCheckError("Unknown variable %s" % self.name)
        self.t = ctx.types[self.name]

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        var = ctx.vars[self.name]
        return builder.load(ctx.vars[self.name], name=self.name)
