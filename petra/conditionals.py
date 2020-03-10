"""
This file defines Petra conditional control flow.
"""

from llvmlite import ir  # type:ignore
from typing import List

from .codegen import CodegenContext
from .expr import Expr
from .statement import Statement
from .type import Bool_t
from .typecheck import TypeContext, TypeCheckError


class If(Statement):
    """
    Directs program flow towards one of two directions depending on a predicate.
    """

    def __init__(self, pred: Expr, then_: List[Statement], else_: List[Statement]):
        self.pred = pred
        self.then_ = then_
        self.else_ = else_
        self.validate()

    def validate(self) -> None:
        self.pred.validate()
        for statement in self.then_:
            statement.validate()
        for statement in self.else_:
            statement.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.pred.typecheck(ctx)
        t_pred = self.pred.get_type()
        if t_pred != Bool_t:
            raise TypeCheckError("If predicate cannot have type %s" % str(t_pred))
        # Typecheck then_ and else_ with a duplicated context
        then_ctx = ctx.copy()
        for statement in self.then_:
            statement.typecheck(then_ctx)
        else_ctx = ctx.copy()
        for statement in self.else_:
            statement.typecheck(else_ctx)

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        pred_value = self.pred.codegen(builder, ctx)
        with builder.if_else(pred_value) as (then_case, else_case):
            with then_case:
                for statement in self.then_:
                    statement.codegen(builder, ctx)
            with else_case:
                for statement in self.else_:
                    statement.codegen(builder, ctx)
