"""
This file defines Petra statements.
"""

import re

from abc import ABC
from llvmlite import ir # type:ignore
from typing import Tuple, Union

from .codegen import codegen_expression, codegen_statement, convert_type, \
        CodegenContext
from .expr import Expr, Var
from .staticcheck import staticcheck, StaticException
from .type import Type
from .typecheck import typecheck, TypeContext, TypeException

#
# Statement
#

class Statement(ABC):
    """
    A Petra statement. Petra functions are composed of statements.
    """
    pass

#
# Assign
#

# Declare is an artifact of Assign, and is not a Statement or any kind of core
# object on its own.
class Declare(object):
    """
    Declares a new variable. Only valid as the assignee in an Assign statement
    or when adding a function.
    """
    def __init__(self, t: Type, name: str):
        self.t = t
        self.name = name

class Assign(Statement):
    """
    Assigns an expression into a possibly new variable.
    """
    def __init__(self, var: Union[Declare, Var], e: Expr):
        self.var = var
        self.e = e
        staticcheck(self)

@staticcheck.register(Assign)
def _staticcheck_assign(s: Assign) -> None:
    if isinstance(s.var, Declare):
        if not re.match(r"^[a-z][a-zA-Z0-9_]*$", s.var.name):
            raise StaticException("Variable name '%s' does not match regex "
                "^[a-z][a-zA-Z0-9_]*$" %s.var.name)
    else:
        staticcheck(s.var)
    staticcheck(s.e)

@typecheck.register(Assign)
def _typecheck_assign(s: Assign, ctx: TypeContext) -> None:
    typecheck(s.e, ctx)
    if isinstance(s.var, Declare):
        if s.var.name in ctx.types:
            raise TypeException("Cannot redeclare variable %s" %s.var.name)
        ctx.types[s.var.name] = s.var.t
    else:
        typecheck(s.var, ctx)
    expected_type = s.e.get_type()
    if ctx.types[s.var.name] != expected_type:
        raise TypeException("Cannot assign expression of type %s to variable of"
            "type %s" %(expected_type, ctx.types[s.var.name]))

@codegen_statement.register(Assign)
def _codegen_statement_assign(s: Assign, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> None:
    exp = codegen_expression(s.e, builder, ctx)
    if isinstance(s.var, Declare):
        ctx.vars[s.var.name] = builder.alloca(convert_type(s.var.t), name=s.var.name)
    builder.store(exp, ctx.vars[s.var.name])

#
# Return
#

class Return(Statement):
    """
    Returns the given expression and ends function execution.
    """
    def __init__(self, e: Union[Tuple[()], Expr]):
        self.e = e
        staticcheck(self)

@staticcheck.register(Return)
def _staticcheck_return(s: Return) -> None:
    if isinstance(s.e, Expr):
        staticcheck(s.e)

@typecheck.register(Return)
def _typecheck_return(s: Return, ctx: TypeContext) -> None:
    if isinstance(s.e, Expr):
        if ctx.return_type == ():
            raise TypeException("Void functions' return statements must return literal ().")
        else:
            typecheck(s.e, ctx)
            if s.e.get_type() != ctx.return_type:
                raise TypeException("Return type %s does not match function declaration." %str(s.e.get_type()))
    else:
        if ctx.return_type != ():
            raise TypeException("Non-void functions cannot return ().")

@codegen_statement.register(Return)
def _codegen_statement_return(s: Return, builder: ir.IRBuilder, ctx: \
        CodegenContext) -> None:
    if isinstance(s.e, Expr):
        value = codegen_expression(s.e, builder, ctx)
        builder.ret(value)
    else:
        builder.ret_void()
