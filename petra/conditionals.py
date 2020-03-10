"""
This file defines Petra conditional control flow.
"""

from llvmlite import ir  # type:ignore
from typing import List

from .codegen import codegen_expression, codegen_statement, CodegenContext
from .expr import Expr
from .statement import Statement
from .validate import validate
from .type import Bool_t
from .typecheck import typecheck, TypeContext, TypeCheckError


class If(Statement):
    """
    Directs program flow towards one of two directions depending on a predicate.
    """

    def __init__(self, pred: Expr, then_: List[Statement], else_: List[Statement]):
        self.pred = pred
        self.then_ = then_
        self.else_ = else_
        validate(self)


@validate.register(If)
def _validate_if(s: If) -> None:
    validate(s.pred)
    for statement in s.then_:
        validate(statement)
    for statement in s.else_:
        validate(statement)


@typecheck.register(If)
def _typecheck_if(s: If, ctx: TypeContext) -> None:
    typecheck(s.pred, ctx)
    t_pred = s.pred.get_type()
    if t_pred != Bool_t:
        raise TypeCheckError("If predicate cannot have type %s" % str(t_pred))
    # Typecheck then_ and else_ with a duplicated context
    then_ctx = ctx.copy()
    for statement in s.then_:
        typecheck(statement, then_ctx)
    else_ctx = ctx.copy()
    for statement in s.else_:
        typecheck(statement, else_ctx)


@codegen_statement.register(If)
def _codegen_statement_if(s: If, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
    pred_value = codegen_expression(s.pred, builder, ctx)
    with builder.if_else(pred_value) as (then_case, else_case):
        with then_case:
            for statement in s.then_:
                codegen_statement(statement, builder, ctx)
        with else_case:
            for statement in s.else_:
                codegen_statement(statement, builder, ctx)
