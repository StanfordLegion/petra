"""
This file defines Petra conditional control flow.
"""

from llvmlite import ir

from .block import Block
from .codegen import CodegenContext
from .expr import Expr
from .statement import Statement
from .type import Bool_t
from .typecheck import TypeContext, TypeCheckError


class If(Statement):
    """
    Directs program flow towards one of two directions depending on a predicate.
    """

    def __init__(self, pred: Expr, then_block: Block, else_block: Block):
        self.pred = pred
        self.then_block = then_block
        self.else_block = else_block
        self.validate()

    def validate(self) -> None:
        self.pred.validate()
        self.then_block.validate()
        self.else_block.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.pred.typecheck(ctx)
        t_pred = self.pred.get_type()
        if t_pred != Bool_t:
            raise TypeCheckError("If predicate cannot have type %s" % str(t_pred))
        then_ctx = ctx.copy()
        self.then_block.typecheck(then_ctx)
        else_ctx = ctx.copy()
        self.else_block.typecheck(else_ctx)

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        pred_value = self.pred.codegen(builder, ctx)
        with builder.if_else(pred_value) as (then_case, else_case):
            with then_case:
                self.then_block.codegen(builder, ctx)
            with else_case:
                self.else_block.codegen(builder, ctx)
