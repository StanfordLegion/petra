"""
This file defines Petra functions.
"""

import re

from llvmlite import ir  # type:ignore
from typing import Dict, List, Tuple

from .codegen import codegen_statement, convert_type, CodegenContext
from .statement import Declare, Statement, Return
from .validate import validate, ValidateError
from .type import Ftypein, Ftypeout, Type
from .typecheck import typecheck, TypeContext, TypeCheckError


class Function(object):
    """
    A Petra function. Petra programs may have one or more functions.
    """

    def __init__(
        self,
        name: str,
        args: Tuple[Declare, ...],
        t_out: Ftypeout,
        statements: List[Statement],
        functypes: Dict[str, Tuple[Ftypein, Ftypeout]],
    ):
        self.name = name
        self.args = args
        self.t_out = t_out
        self.statements = statements
        validate(self)
        # Initial typecontext should contain arguments
        ctx = TypeContext(functypes, t_out)
        for arg in self.args:
            if arg.name in ctx.types:
                raise TypeCheckError("Cannot redeclare variable %s" % arg.name)
            ctx.types[arg.name] = arg.t
        typecheck(self, ctx)

    def codegen(self, module: ir.Module, funcs: Dict[str, ir.Function]) -> None:
        block = funcs[self.name].append_basic_block(name="start")
        builder = ir.IRBuilder(block)
        ctx = CodegenContext(funcs)
        # Treat function arguments as variables declared at the beginning.
        for i, arg in enumerate(self.args):
            var = builder.alloca(convert_type(arg.t), name=arg.name)
            builder.store(funcs[self.name].args[i], var)
            ctx.vars[arg.name] = var
        for statement in self.statements:
            codegen_statement(statement, builder, ctx)


@validate.register(Function)
def _validate_function(f: Function) -> None:
    # check for valid name
    if not re.match(r"^[a-z][a-zA-Z0-9_]*$", f.name):
        raise ValidateError(
            "Function name '%s' does not match regex " "^[a-z][a-zA-Z0-9_]*$" % f.name
        )
    # check for valid arg names
    for arg in f.args:
        if not re.match(r"^[a-z][a-zA-Z0-9_]*$", arg.name):
            raise ValidateError(
                "Argument '%s' does not match regex " "^[a-z][a-zA-Z0-9_]*$" % arg.name
            )
    # check for inaccessible return statements
    # TODO: This needs to be updated to take branching logic into account.
    # It can be viewed as a DAG where every path must end in a return with
    # nothing after.
    found_first_return = False
    for statement in f.statements:
        validate(statement)
        if isinstance(statement, Return):
            if found_first_return:
                raise ValidateError("Found inaccessible return statement.")
            found_first_return = True


@typecheck.register(Function)
def _typecheck_function(f: Function, ctx: TypeContext) -> None:
    for statement in f.statements:
        typecheck(statement, ctx)
