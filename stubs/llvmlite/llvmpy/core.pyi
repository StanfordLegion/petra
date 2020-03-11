from llvmlite import ir as ir
from typing import Any

CallOrInvokeInstruction: Any

class LLVMException(Exception): ...

ICMP_EQ: Any
ICMP_NE: Any
ICMP_SLT: Any
ICMP_SLE: Any
ICMP_SGT: Any
ICMP_SGE: Any
ICMP_ULT: Any
ICMP_ULE: Any
ICMP_UGT: Any
ICMP_UGE: Any
FCMP_OEQ: Any
FCMP_OGT: Any
FCMP_OGE: Any
FCMP_OLT: Any
FCMP_OLE: Any
FCMP_ONE: Any
FCMP_ORD: Any
FCMP_UEQ: Any
FCMP_UGT: Any
FCMP_UGE: Any
FCMP_ULT: Any
FCMP_ULE: Any
FCMP_UNE: Any
FCMP_UNO: Any
INTR_FABS: str
INTR_EXP: str
INTR_LOG: str
INTR_LOG10: str
INTR_SIN: str
INTR_COS: str
INTR_POWI: str
INTR_POW: str
INTR_FLOOR: str
LINKAGE_EXTERNAL: str
LINKAGE_INTERNAL: str
LINKAGE_LINKONCE_ODR: str
ATTR_NO_CAPTURE: str

class Type:
    @staticmethod
    def int(width: int = ...): ...
    @staticmethod
    def float(): ...
    @staticmethod
    def half(): ...
    @staticmethod
    def double(): ...
    @staticmethod
    def pointer(ty: Any, addrspace: int = ...): ...
    @staticmethod
    def function(res: Any, args: Any, var_arg: bool = ...): ...
    @staticmethod
    def struct(members: Any): ...
    @staticmethod
    def array(element: Any, count: Any): ...
    @staticmethod
    def void(): ...

class Constant:
    @staticmethod
    def all_ones(ty: Any): ...
    @staticmethod
    def int(ty: Any, n: Any): ...
    @staticmethod
    def int_signextend(ty: Any, n: Any): ...
    @staticmethod
    def real(ty: Any, n: Any): ...
    @staticmethod
    def struct(elems: Any): ...
    @staticmethod
    def null(ty: Any): ...
    @staticmethod
    def undef(ty: Any): ...
    @staticmethod
    def stringz(string: Any): ...
    @staticmethod
    def array(typ: Any, val: Any): ...
    @staticmethod
    def bitcast(const: Any, typ: Any): ...
    @staticmethod
    def inttoptr(const: Any, typ: Any): ...
    @staticmethod
    def gep(const: Any, indices: Any): ...

class Module(ir.Module):
    def get_or_insert_function(self, fnty: Any, name: Any): ...
    def verify(self) -> None: ...
    def add_function(self, fnty: Any, name: Any): ...
    def add_global_variable(self, ty: Any, name: Any, addrspace: int = ...): ...
    def get_global_variable_named(self, name: Any): ...
    def get_or_insert_named_metadata(self, name: Any): ...

class Function(ir.Function):
    @classmethod
    def new(cls, module_obj: Any, functy: Any, name: str = ...): ...
    @staticmethod
    def intrinsic(module: Any, intrinsic: Any, tys: Any): ...

class Builder(ir.IRBuilder):
    def icmp(self, pred: Any, lhs: Any, rhs: Any, name: str = ...): ...
    def fcmp(self, pred: Any, lhs: Any, rhs: Any, name: str = ...): ...

class MetaDataString(ir.MetaDataString):
    @staticmethod
    def get(module: Any, text: Any): ...

class MetaData:
    @staticmethod
    def get(module: Any, values: Any): ...

class InlineAsm(ir.InlineAsm):
    @staticmethod
    def get(*args: Any, **kwargs: Any): ...
