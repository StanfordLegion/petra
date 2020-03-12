"""
This file defines Petra functions.
"""

import re

from llvmlite import ir
from typing import Dict, List, Tuple

from .block import Block
from .codegen import CodegenContext
from .statement import Statement, Return
from .symbol import Symbol
from .type import Ftypein, Ftypeout, Type
from .typecheck import TypeContext, TypeCheckError
from .validate import ValidateError


class Function(object):
    """
    A Petra function. Petra programs may have one or more functions.
    """

    def __init__(
        self,
        name: str,
        args: Tuple[Symbol, ...],
        t_out: Ftypeout,
        block: Block,
        functypes: Dict[str, Tuple[Ftypein, Ftypeout]],
    ):
        self.name = name
        self.args = args
        self.t_out = t_out
        self.block = block
        self.validate()
        # Initial typecontext should contain arguments
        ctx = TypeContext(functypes, t_out)
        for arg in self.args:
            if arg in ctx.variables:
                raise TypeCheckError("Parameter '%s' declared multiple times" % arg)
            ctx.variables.add(arg)
        self.typecheck(ctx)

    def validate(self) -> None:
        # check for valid name
        if not re.match(r"^[a-z][a-zA-Z0-9_]*$", self.name):
            raise ValidateError(
                "Function name '%s' does not match regex "
                "^[a-z][a-zA-Z0-9_]*$" % self.name
            )
        # check for valid arg names
        for arg in self.args:
            if not re.match(r"^[a-z][a-zA-Z0-9_]*$", arg.name):
                raise ValidateError(
                    "Argument '%s' does not match regex "
                    "^[a-z][a-zA-Z0-9_]*$" % arg.name
                )
        self.block.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.block.typecheck(ctx)

    def codegen(self, module: ir.Module, funcs: Dict[str, ir.Function]) -> None:
        block = funcs[self.name].append_basic_block(name="start")
        builder = ir.IRBuilder(block)
        ctx = CodegenContext(funcs)
        # Treat function arguments as variables declared at the beginning.
        for i, arg in enumerate(self.args):
            var = builder.alloca(arg.get_type().llvm_type(), name=arg.unique_name())
            # FIXME: I'm not sure why I can't get this to type check
            builder.store(funcs[self.name].args[i], var)  # type: ignore
            ctx.vars[arg] = var
        self.block.codegen(builder, ctx)
