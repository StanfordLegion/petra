from typing import cast, Callable

import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int8, c_int16, c_int32, c_int64

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

# Int16_t functions.

# TODO(adbenson): refactor this to take in arguments for better testing

a16 = pt.Symbol(pt.Int16_t, "a16")
b16 = pt.Symbol(pt.Int16_t, "b16")
c16 = pt.Symbol(pt.Int16_t, "c16")
d16 = pt.Symbol(pt.Int16_t, "d16")
e16 = pt.Symbol(pt.Int16_t, "e16")
f16 = pt.Symbol(pt.Int16_t, "f16")
g16 = pt.Symbol(pt.Int16_t, "g16")
h16 = pt.Symbol(pt.Int16_t, "h16")
i16 = pt.Symbol(pt.Int16_t, "i16")

program.add_func(
    "add_i16",
    (),
    pt.Int16_t,
    pt.Block(
        [
            pt.DefineVar(a16, pt.Add(pt.Int16(-11), pt.Int16(-4))),
            pt.DefineVar(b16, pt.Add(pt.Int16(-11), pt.Int16(0))),
            pt.DefineVar(c16, pt.Add(pt.Int16(-11), pt.Int16(7))),
            pt.DefineVar(d16, pt.Add(pt.Int16(0), pt.Int16(-5))),
            pt.DefineVar(e16, pt.Add(pt.Int16(0), pt.Int16(0))),
            pt.DefineVar(f16, pt.Add(pt.Int16(0), pt.Int16(3))),
            pt.DefineVar(g16, pt.Add(pt.Int16(7), pt.Int16(-8))),
            pt.DefineVar(h16, pt.Add(pt.Int16(7), pt.Int16(0))),
            pt.DefineVar(i16, pt.Add(pt.Int16(7), pt.Int16(8))),
            pt.Return(
                pt.Add(
                    pt.Var(a16),
                    pt.Add(
                        pt.Var(b16),
                        pt.Add(
                            pt.Var(c16),
                            pt.Add(
                                pt.Var(d16),
                                pt.Add(
                                    pt.Var(e16),
                                    pt.Add(
                                        pt.Var(f16),
                                        pt.Add(
                                            pt.Var(g16),
                                            pt.Add(pt.Var(h16), pt.Var(i16)),
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


# Int64_t functions.

# TODO(adbenson): refactor this to take in arguments for better testing

a64 = pt.Symbol(pt.Int64_t, "a64")
b64 = pt.Symbol(pt.Int64_t, "b64")
c64 = pt.Symbol(pt.Int64_t, "c64")
d64 = pt.Symbol(pt.Int64_t, "d64")
e64 = pt.Symbol(pt.Int64_t, "e64")
f64 = pt.Symbol(pt.Int64_t, "f64")
g64 = pt.Symbol(pt.Int64_t, "g64")
h64 = pt.Symbol(pt.Int64_t, "h64")
i64 = pt.Symbol(pt.Int64_t, "i64")

program.add_func(
    "add_i64",
    (),
    pt.Int64_t,
    pt.Block(
        [
            pt.DefineVar(a64, pt.Add(pt.Int64(-11), pt.Int64(-4))),
            pt.DefineVar(b64, pt.Add(pt.Int64(-11), pt.Int64(0))),
            pt.DefineVar(c64, pt.Add(pt.Int64(-11), pt.Int64(7))),
            pt.DefineVar(d64, pt.Add(pt.Int64(0), pt.Int64(-5))),
            pt.DefineVar(e64, pt.Add(pt.Int64(0), pt.Int64(0))),
            pt.DefineVar(f64, pt.Add(pt.Int64(0), pt.Int64(3))),
            pt.DefineVar(g64, pt.Add(pt.Int64(7), pt.Int64(-8))),
            pt.DefineVar(h64, pt.Add(pt.Int64(7), pt.Int64(0))),
            pt.DefineVar(i64, pt.Add(pt.Int64(7), pt.Int64(8))),
            pt.Return(
                pt.Add(
                    pt.Var(a64),
                    pt.Add(
                        pt.Var(b64),
                        pt.Add(
                            pt.Var(c64),
                            pt.Add(
                                pt.Var(d64),
                                pt.Add(
                                    pt.Var(e64),
                                    pt.Add(
                                        pt.Var(f64),
                                        pt.Add(
                                            pt.Var(g64),
                                            pt.Add(pt.Var(h64), pt.Var(i64)),
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

        add_i16 = self.engine.get_function_address("add_i16")
        self.add_i16 = cast(Callable[[], int], CFUNCTYPE(c_int16)(add_i16))

        add_i32 = self.engine.get_function_address("add_i32")
        self.add_i32 = cast(Callable[[], int], CFUNCTYPE(c_int32)(add_i32))

        add_i64 = self.engine.get_function_address("add_i64")
        self.add_i64 = cast(Callable[[], int], CFUNCTYPE(c_int64)(add_i64))

    def test_add_i8(self) -> None:
        self.assertEqual(self.add_i8(), -11)

    def test_add_i16(self) -> None:
        self.assertEqual(self.add_i16(), -11)

    def test_add_i32(self) -> None:
        self.assertEqual(self.add_i32(), -11)

    def test_add_i64(self) -> None:
        self.assertEqual(self.add_i64(), -11)

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
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Add(pt.Int16(2), pt.Int64(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Add(pt.Int64(2), pt.Int16(2)))]),
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
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Sub(pt.Int16(2), pt.Int64(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Sub(pt.Int64(2), pt.Int16(2)))]),
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
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Mul(pt.Int16(2), pt.Int64(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Mul(pt.Int64(2), pt.Int16(2)))]),
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
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Div(pt.Int16(2), pt.Int64(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Div(pt.Int64(2), pt.Int16(2)))]),
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
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Mod(pt.Int16(2), pt.Int64(2)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int64_t,
                pt.Block([pt.Return(pt.Mod(pt.Int64(2), pt.Int16(2)))]),
            )
