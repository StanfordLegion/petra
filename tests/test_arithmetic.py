from typing import cast, Callable

import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int8, c_int32

program = pt.Program("module")

# Int8_t functions.

# TODO(adbenson): refactor this to take in arguments for better testing

a = pt.Symbol(pt.Int8_t, "a")
b = pt.Symbol(pt.Int8_t, "b")
c = pt.Symbol(pt.Int8_t, "c")
d = pt.Symbol(pt.Int8_t, "d")
e = pt.Symbol(pt.Int8_t, "e")
f = pt.Symbol(pt.Int8_t, "f")
g = pt.Symbol(pt.Int8_t, "g")
h = pt.Symbol(pt.Int8_t, "h")
i = pt.Symbol(pt.Int8_t, "i")

program.add_func(
    "add_i8",
    (),
    pt.Int8_t,
    pt.Block(
        [
            pt.DefineVar(a, pt.Add(pt.Int8(-11), pt.Int8(-4))),
            pt.DefineVar(b, pt.Add(pt.Int8(-11), pt.Int8(0))),
            pt.DefineVar(c, pt.Add(pt.Int8(-11), pt.Int8(7))),
            pt.DefineVar(d, pt.Add(pt.Int8(0), pt.Int8(-5))),
            pt.DefineVar(e, pt.Add(pt.Int8(0), pt.Int8(0))),
            pt.DefineVar(f, pt.Add(pt.Int8(0), pt.Int8(3))),
            pt.DefineVar(g, pt.Add(pt.Int8(7), pt.Int8(-8))),
            pt.DefineVar(h, pt.Add(pt.Int8(7), pt.Int8(0))),
            pt.DefineVar(i, pt.Add(pt.Int8(7), pt.Int8(8))),
            pt.Return(
                pt.Add(
                    pt.Var(a),
                    pt.Add(
                        pt.Var(b),
                        pt.Add(
                            pt.Var(c),
                            pt.Add(
                                pt.Var(d),
                                pt.Add(
                                    pt.Var(e),
                                    pt.Add(
                                        pt.Var(f),
                                        pt.Add(
                                            pt.Var(g), pt.Add(pt.Var(h), pt.Var(i)),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                )
            ),
        ]
    ),
)

# Int32_t functions.

# TODO(adbenson): refactor this to take in arguments for better testing

a32 = pt.Symbol(pt.Int32_t, "a32")
b32 = pt.Symbol(pt.Int32_t, "b32")
c32 = pt.Symbol(pt.Int32_t, "c32")
d32 = pt.Symbol(pt.Int32_t, "d32")
e32 = pt.Symbol(pt.Int32_t, "e32")
f32 = pt.Symbol(pt.Int32_t, "f32")
g32 = pt.Symbol(pt.Int32_t, "g32")
h32 = pt.Symbol(pt.Int32_t, "h32")
i32 = pt.Symbol(pt.Int32_t, "i32")

program.add_func(
    "add_i32",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(a32, pt.Add(pt.Int32(-11), pt.Int32(-4))),
            pt.DefineVar(b32, pt.Add(pt.Int32(-11), pt.Int32(0))),
            pt.DefineVar(c32, pt.Add(pt.Int32(-11), pt.Int32(7))),
            pt.DefineVar(d32, pt.Add(pt.Int32(0), pt.Int32(-5))),
            pt.DefineVar(e32, pt.Add(pt.Int32(0), pt.Int32(0))),
            pt.DefineVar(f32, pt.Add(pt.Int32(0), pt.Int32(3))),
            pt.DefineVar(g32, pt.Add(pt.Int32(7), pt.Int32(-8))),
            pt.DefineVar(h32, pt.Add(pt.Int32(7), pt.Int32(0))),
            pt.DefineVar(i32, pt.Add(pt.Int32(7), pt.Int32(8))),
            pt.Return(
                pt.Add(
                    pt.Var(a32),
                    pt.Add(
                        pt.Var(b32),
                        pt.Add(
                            pt.Var(c32),
                            pt.Add(
                                pt.Var(d32),
                                pt.Add(
                                    pt.Var(e32),
                                    pt.Add(
                                        pt.Var(f32),
                                        pt.Add(
                                            pt.Var(g32),
                                            pt.Add(pt.Var(h32), pt.Var(i32)),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                )
            ),
        ]
    ),
)


class ConstantsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        add_i8 = self.engine.get_function_address("add_i8")
        self.add_i8 = cast(Callable[[], int], CFUNCTYPE(c_int8)(add_i8))

        add_i32 = self.engine.get_function_address("add_i32")
        self.add_i32 = cast(Callable[[], int], CFUNCTYPE(c_int32)(add_i32))

    def test_add_i8(self) -> None:
        self.assertEqual(self.add_i8(), -11)

    def test_add_i32(self) -> None:
        self.assertEqual(self.add_i32(), -11)

    def test_mismatch_type_add(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Add(pt.Int8(2), pt.Int32(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Add(pt.Int32(2), pt.Int8(2)))]),
            )

    def test_mismatch_type_sub(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Sub(pt.Int8(2), pt.Int32(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Sub(pt.Int32(2), pt.Int8(2)))]),
            )

    def test_mismatch_type_mul(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Mul(pt.Int8(2), pt.Int32(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Mul(pt.Int32(2), pt.Int8(2)))]),
            )

    def test_mismatch_type_div(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Div(pt.Int8(2), pt.Int32(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Div(pt.Int32(2), pt.Int8(2)))]),
            )

    def test_mismatch_type_mod(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Mod(pt.Int8(2), pt.Int32(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Mod(pt.Int32(2), pt.Int8(2)))]),
            )
