"""
This file defines Petra blocks.
"""

from llvmlite import ir  # type:ignore
from typing import List, Union

from .codegen import CodegenContext
from .expr import Expr
from .statement import Return, Statement
from .validate import ValidateError
from .typecheck import TypeContext


class Block(object):
    """
    A block of statements.
    """

    def __init__(self, statements: List[Union[Expr, Statement]]):
        self.statements = statements
        self.validate()

    def validate(self) -> None:
        # TODO: This needs to be updated to take branching logic into account.
        # It can be viewed as a DAG where every path must end in a return with
        # nothing after.
        found_return = False
        for statement in self.statements:
            statement.validate()
            if found_return:
                raise ValidateError("Found inaccessible statement.")
            if isinstance(statement, Return):
                found_return = True

    def typecheck(self, ctx: TypeContext) -> None:
        for statement in self.statements:
            statement.typecheck(ctx)

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        for statement in self.statements:
            statement.codegen(builder, ctx)
