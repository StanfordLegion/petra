from typing import cast, Callable

import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32

program = pt.Program("module")

x = pt.Symbol(pt.Int32_t, "x")
y = pt.Symbol(pt.Int32_t, "y")
z = pt.Symbol(pt.Int8_t, "z")

program.add_func(
    "return_temp",
    (),
    pt.Int32_t,
    pt.Block([pt.DefineVar(x, pt.Int32(2)), pt.Return(pt.Var(x))]),
)

program.add_func(
    "return_shuffle_temp",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(x, pt.Int32(2)),
            pt.DefineVar(y, pt.Var(x)),
            pt.Return(pt.Var(y)),
        ]
    ),
)

program.add_func(
    "temp_unused",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(x, pt.Int32(500)),
            pt.DefineVar(y, pt.Var(x)),
            pt.Return(pt.Int32(2)),
        ]
    ),
)

program.add_func(
    "return_temp_unused",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(x, pt.Int32(2)),
            pt.DefineVar(y, pt.Var(x)),
            pt.Return(pt.Var(x)),
        ]
    ),
)


class VarsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        return_temp = self.engine.get_function_address("return_temp")
        self.return_temp = cast(Callable[[], int], CFUNCTYPE(c_int32)(return_temp))

        return_shuffle_temp = self.engine.get_function_address("return_shuffle_temp")
        self.return_shuffle_temp = cast(
            Callable[[], int], CFUNCTYPE(c_int32)(return_shuffle_temp)
        )

        temp_unused = self.engine.get_function_address("temp_unused")
        self.temp_unused = cast(Callable[[], int], CFUNCTYPE(c_int32)(temp_unused))

        return_temp_unused = self.engine.get_function_address("return_temp_unused")
        self.return_temp_unused = cast(
            Callable[[], int], CFUNCTYPE(c_int32)(return_temp_unused)
        )

    def test_return_temp(self) -> None:
        self.assertEqual(self.return_temp(), 2)

    def test_return_shuffle_temp(self) -> None:
        self.assertEqual(self.return_shuffle_temp(), 2)

    def test_temp_unused(self) -> None:
        self.assertEqual(self.temp_unused(), 2)

    def test_return_temp_unused(self) -> None:
        self.assertEqual(self.return_temp_unused(), 2)

    def test_variable_name_starts_not_lowercase(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "_")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "_a")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "A")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "Aa")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "0")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "0a")
        pt.Symbol(pt.Int32_t, "a")
        pt.Symbol(pt.Int32_t, "aa")

    def test_variable_name_contains_forbidden(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "a*")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "a-a")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "a+a")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "a🤔")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "a猫")
        with self.assertRaises(pt.ValidateError):
            pt.Symbol(pt.Int32_t, "a ")
        pt.Symbol(pt.Int32_t, "aBCD")
        pt.Symbol(pt.Int32_t, "a_B_02")
        pt.Symbol(pt.Int32_t, "a554")

    def test_declare_undeclared_variable(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.DefineVar(x, pt.Var(x)), pt.Return(pt.Int32(2)),]),
            )

    def test_assign_undeclared_variable(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block(
                    [pt.Assign(pt.Var(x), pt.Int32(500)), pt.Return(pt.Int32(2)),]
                ),
            )

    def test_return_undeclared_variable(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, pt.Block([pt.Return(pt.Var(x))])
            )

    def test_redeclared_variable(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block(
                    [
                        pt.DefineVar(x, pt.Int32(2)),
                        pt.DefineVar(x, pt.Int32(3)),
                        pt.Return(pt.Int32(2)),
                    ]
                ),
            )

    def test_declare_wrong_type(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.DefineVar(z, pt.Int32(2)), pt.Return(pt.Int32(2)),]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.DefineVar(x, pt.Int8(2)), pt.Return(pt.Int32(2)),]),
            )
