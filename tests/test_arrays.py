from typing import cast, Callable

import subprocess
import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32

program = pt.Program("module")

My_Array = pt.ArrayType(pt.Int32_t, 3)
array_var = pt.Symbol(My_Array, "array_var")

program.add_func(
    "array_set_get_values",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(array_var),
            pt.Assign(
                pt.Var(array_var), pt.SetElement(pt.Var(array_var), pt.Int32(1), 0)
            ),
            pt.Assign(
                pt.Var(array_var), pt.SetElement(pt.Var(array_var), pt.Int32(2), 1)
            ),
            pt.Assign(
                pt.Var(array_var), pt.SetElement(pt.Var(array_var), pt.Int32(3), 2)
            ),
            pt.Return(
                pt.Add(
                    pt.GetElement(pt.Var(array_var), 0),
                    pt.Add(
                        pt.GetElement(pt.Var(array_var), 1),
                        pt.GetElement(pt.Var(array_var), 2),
                    ),
                )
            ),
        ]
    ),
)


class ArraysTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        array_set_get_values = self.engine.get_function_address("array_set_get_values")
        self.array_set_get_values = cast(
            Callable[[], int], CFUNCTYPE(c_int32)(array_set_get_values)
        )

    def test_array_set_get_values(self) -> None:
        self.assertEqual(self.array_set_get_values(), 6)
