"""
This package defines the Petra library.
"""

from .arithmetic import Add, Sub, Mul, Div, Mod
from .call import Call
from .conditionals import If
from .constant import Bool, Float, Int8, Int32
from .expr import Var
from .program import Program
from .statement import Declare, Assign, Return
from .staticcheck import StaticException
from .truth import And, Eq, Gt, Gte, Lt, Lte, Neq, Not, Or
from .type import Bool_t, Float_t, Int8_t, Int32_t
from .typecheck import TypeException
