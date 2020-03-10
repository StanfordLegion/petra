"""
This file defines Petra function call expressions and statements.
"""

import re

from llvmlite import ir  # type:ignore
from typing import List, Optional, Tuple, Union

from .codegen import codegen_expression, codegen_statement, CodegenContext
from .expr import Expr
from .statement import Statement
from .validate import validate, ValidateError
from .type import Type
from .typecheck import typecheck, TypeContext, TypeCheckError


class Call(Expr, Statement):
    """
    A function call that returns a value.
    """

    def __init__(self, name: str, args: List[Expr]):
        self.name = name
        self.args = args
        self.t: Union[Tuple[()], Optional[Type]] = None
        validate(self)

    def get_type(self) -> Type:
        if isinstance(self.t, Type):
            return self.t
        if self.t == ():
            raise TypeCheckError("Attempted to use Call statement as expression")
        raise Exception("Expected type to exist - was typecheck called?")


@validate.register(Call)
def _validate_call(c: Call) -> None:
    if not re.match(r"^[a-z][a-zA-Z0-9_]*$", c.name):
        raise ValidateError(
            "Function call to '%s' does not match regex "
            "^[a-z][a-zA-Z0-9_]*$" % c.name
        )


@typecheck.register(Call)
def _typecheck_call(c: Call, ctx: TypeContext) -> None:
    # check existence of name
    if c.name not in ctx.functypes:
        raise TypeCheckError("Undeclared function '%s'" % c.name)
    (t_in, t_out) = ctx.functypes[c.name]
    # check argument types
    if len(c.args) != len(t_in):
        raise TypeCheckError(
            "Function call to '%s' expects %s arguments, not %s"
            % (c.name, len(t_in), len(c.args))
        )
    for i, arg in enumerate(c.args):
        typecheck(arg, ctx)
        if arg.get_type() != t_in[i]:
            raise TypeCheckError(
                "Argument %s of call to '%s' should be of type"
                "%s, not %s" % (i, c.name, str(t_in[i]), str(arg.get_type()))
            )
    c.t = t_out


def _codegen(c: Call, builder: ir.IRBuilder, ctx: CodegenContext):
    args = tuple(map(lambda arg: codegen_expression(arg, builder, ctx), c.args))
    func = ctx.funcs[c.name]
    return builder.call(func, args)


@codegen_expression.register(Call)
def _codegen_expression_call(
    c: Call, builder: ir.IRBuilder, ctx: CodegenContext
) -> ir.Value:
    return _codegen(c, builder, ctx)


@codegen_statement.register(Call)
def _codegen_statement_call(
    c: Call, builder: ir.IRBuilder, ctx: CodegenContext
) -> None:
    _codegen(c, builder, ctx)
