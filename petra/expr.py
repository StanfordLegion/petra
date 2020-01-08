"""
This file defines Petra expressions.
"""

import re

from abc import ABC, abstractmethod
from llvmlite import ir  # type:ignore
from typing import Optional

from .codegen import codegen_expression, CodegenContext
from .staticcheck import staticcheck, StaticException
from .type import Type
from .typecheck import typecheck, TypeContext, TypeException


class Expr(ABC):
    """
    A Petra expression. Expressions have a type and can be evaluated.
    """

    @abstractmethod
    def get_type(self) -> Type:
        """
        Returns the Petra type of the expression.

        This function can only be called after typecheck() is called on self.
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
        staticcheck(self)

    def get_type(self) -> Type:
        if isinstance(self.t, Type):
            return self.t
        raise Exception("Expected type to exist - was typecheck called?")


@staticcheck.register(Var)
def _staticcheck_var(v: Var) -> None:
    if not re.match(r"^[a-z][a-zA-Z0-9_]*$", v.name):
        raise StaticException(
            "Variable name '%s' does not match regex " "^[a-z][a-zA-Z0-9_]*$" % v.name
        )


@typecheck.register(Var)
def _typecheck_var(v: Var, ctx: TypeContext) -> None:
    if v.name not in ctx.types:
        raise TypeException("Unknown variable %s" % v.name)
    v.t = ctx.types[v.name]


@codegen_expression.register(Var)
def _codegen_expression_var(
    v: Var, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    var = ctx.vars[v.name]
    return builder.load(ctx.vars[v.name], name=v.name)
