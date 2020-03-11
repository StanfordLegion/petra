"""
This package defines the Petra library.
"""

from .arithmetic import Add, Sub, Mul, Div, Mod
from .block import Block
from .call import Call
from .conditionals import If
from .constant import Bool, Float32, Float64, Int8, Int32
from .expr import Var
from .program import Program
from .statement import Declare, Assign, Return
from .validate import ValidateError
from .truth import And, Eq, Gt, Gte, Lt, Lte, Neq, Not, Or
from .type import Bool_t, Float32_t, Float64_t, Int8_t, Int32_t
from .typecheck import TypeCheckError
