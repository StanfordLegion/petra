"""
This file defines Petra function call expressions and statements.
"""

import re

from llvmlite import ir  # type:ignore
from typing import List, Optional, Tuple, Union

from .codegen import CodegenContext
from .expr import Expr
from .statement import Statement
from .validate import ValidateError
from .type import Type
from .typecheck import TypeContext, TypeCheckError


class Call(Expr):
    """
    A function call expression.
    """

    def __init__(self, name: str, args: List[Expr]):
        self.name = name
        self.args = args
        self.t: Union[Tuple[()], Optional[Type]] = None
        self.validate()

    def get_type(self) -> Type:
        if isinstance(self.t, Type):
            return self.t
        if self.t == ():
            raise TypeCheckError("Attempted to use Call statement as expression")
        raise Exception("Expected type to exist - was typecheck called?")

    def validate(self) -> None:
        if not re.match(r"^[a-z][a-zA-Z0-9_]*$", self.name):
            raise ValidateError(
                "Function call to '%s' does not match regex "
                "^[a-z][a-zA-Z0-9_]*$" % self.name
            )

    def typecheck(self, ctx: TypeContext) -> None:
        # check existence of name
        if self.name not in ctx.functypes:
            raise TypeCheckError("Undeclared function '%s'" % self.name)
        (t_in, t_out) = ctx.functypes[self.name]
        # check argument types
        if len(self.args) != len(t_in):
            raise TypeCheckError(
                "Function call to '%s' expects %s arguments, not %s"
                % (self.name, len(t_in), len(self.args))
            )
        for i, arg in enumerate(self.args):
            arg.typecheck(ctx)
            if arg.get_type() != t_in[i]:
                raise TypeCheckError(
                    "Argument %s of call to '%s' should be of type"
                    "%s, not %s" % (i, self.name, str(t_in[i]), str(arg.get_type()))
                )
        self.t = t_out

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> ir.Value:
        args = tuple(map(lambda arg: arg.codegen(builder, ctx), self.args))
        func = ctx.funcs[self.name]
        return builder.call(func, args)
