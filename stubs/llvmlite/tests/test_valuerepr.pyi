from . import TestCase as TestCase
from llvmlite.ir import (
    ArrayType as ArrayType,
    Constant as Constant,
    DoubleType as DoubleType,
    FloatType as FloatType,
    HalfType as HalfType,
    IntType as IntType,
    LiteralStructType as LiteralStructType,
)
from typing import Any

int8: Any
int16: Any
PY36_OR_LATER: Any

class TestValueRepr(TestCase):
    def test_double_repr(self) -> None: ...
    def test_float_repr(self) -> None: ...
    def test_half_repr(self) -> None: ...
    def test_struct_repr(self) -> None: ...
    def test_array_repr(self) -> None: ...
