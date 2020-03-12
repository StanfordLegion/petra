"""
This file defines the codegen context and helpers.
"""

from llvmlite import ir
from typing import Dict, Tuple

from .symbol import Symbol
from .type import Ftypein, Ftypeout, Type


class CodegenContext(object):
    """
    A context of variables for use in codegen.
    """

    def __init__(self, funcs: Dict[str, ir.Function]):
        self.vars: Dict[Symbol, ir.Value] = dict()
        self.funcs: Dict[str, ir.Function] = funcs


def convert_func_type(t_in: Ftypein, t_out: Ftypeout) -> ir.FunctionType:
    llvm_t_in: Tuple[ir.Type, ...] = ()

    def convert_type(t: Type) -> ir.Type:
        return t.llvm_type()

    if len(t_in) > 0:
        llvm_t_in = tuple(map(convert_type, t_in))
    llvm_t_out: ir.Type = ir.VoidType()
    if isinstance(t_out, Type):
        llvm_t_out = t_out.llvm_type()
    return ir.FunctionType(llvm_t_out, llvm_t_in)
