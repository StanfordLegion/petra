"""
This file defines Petra conditional control flow.
"""

import contextlib
from typing import ContextManager, Callable

from llvmlite import ir
from llvmlite.ir import builder

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


def _label_suffix(label: str, suffix: str) -> str:
    """Returns (label + suffix) or a truncated version if it's too long.
    Parameters
    ----------
    label : str
        Label name
    suffix : str
        Label suffix
    """
    if len(label) > 50:
        nhead = 25
        return "".join([label[:nhead], "..", suffix])
    else:
        return label + suffix


@contextlib.contextmanager  # type: ignore
def while_then(
    self: ir.IRBuilder, pred: Callable[[], ir.Value]
) -> ContextManager[ir.Block]:
    """
    A context manager which sets up a conditional basic block based
    on the given predicate (a i1 value).  If the conditional block
    is not explicitly terminated, a branch will be added to the next
    block.
    """
    bb = self.basic_block
    bbwhile = self.append_basic_block(name=_label_suffix(bb.name, ".while"))
    bbend = self.append_basic_block(name=_label_suffix(bb.name, ".endwhile"))

    br = self.cbranch(pred(), bbwhile, bbend)

    with self._branch_helper(bbwhile, bbend):
        yield bbend
        if self.basic_block.terminator is None:
            br = self.cbranch(pred(), bbwhile, bbend)

    self.position_at_end(bbend)


class While(Statement):
    def __init__(self, pred: Expr, while_block: Block):
        self.pred = pred
        self.while_block = while_block
        self.validate()

    def validate(self) -> None:
        self.pred.validate()
        self.while_block.validate()

    def typecheck(self, ctx: TypeContext) -> None:
        self.pred.typecheck(ctx)
        t_pred = self.pred.get_type()
        if t_pred != Bool_t:
            raise TypeCheckError("While predicate cannot have type %s" % str(t_pred))
        while_ctx = ctx.copy()
        self.while_block.typecheck(while_ctx)

    def codegen(self, builder: ir.IRBuilder, ctx: CodegenContext) -> None:
        def pred() -> ir.Value:
            return self.pred.codegen(builder, ctx)

        with while_then(builder, pred):
            self.while_block.codegen(builder, ctx)
