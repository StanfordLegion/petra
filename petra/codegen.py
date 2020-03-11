"""
This file defines the codegen context and helpers.
"""

from llvmlite import ir
from typing import Dict, Tuple

from .type import Bool_t, Float_t, Ftypein, Ftypeout, Int8_t, Int32_t, Type


class CodegenContext(object):
    """
    A context of variables for use in codegen.
    """

    def __init__(self, funcs: Dict[str, ir.Function]):
        self.vars: Dict[str, ir.Value] = dict()
        self.funcs: Dict[str, ir.Function] = funcs


def convert_func_type(t_in: Ftypein, t_out: Ftypeout):
    llvm_t_in: Tuple[ir.Type, ...] = ()
    if len(t_in) > 0:
        llvm_t_in = tuple(map(convert_type, t_in))
    llvm_t_out: ir.Type = ir.VoidType()
    if isinstance(t_out, Type):
        llvm_t_out = convert_type(t_out)
    return ir.FunctionType(llvm_t_out, llvm_t_in)


def convert_type(t: Type) -> ir.Type:
    if t == Bool_t:
        return ir.IntType(1)
    elif t == Float_t:
        return ir.FloatType()
    elif t == Int8_t:
        return ir.IntType(8)
    elif t == Int32_t:
        return ir.IntType(32)
    else:
        raise NotImplementedError("Unsupported type: " + str(t))
