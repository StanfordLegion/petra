"""
This package defines the Petra library.
"""

from .arithmetic import Add, Sub, Mul, Div, Mod
from .block import Block
from .call import Call
from .conditionals import If, While
from .constant import Bool, Float32, Float64, Int8, Int16, Int32, Int64
from .expr import Var
from .program import Program
from .statement import Assign, DefineVar, Return
from .symbol import Symbol
from .validate import ValidateError
from .truth import And, Eq, Gt, Gte, Lt, Lte, Neq, Not, Or
from .type import Bool_t, Float32_t, Float64_t, Int8_t, Int16_t, Int32_t, Int64_t
from .typecheck import TypeCheckError
