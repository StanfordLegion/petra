import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int8, c_int32

program = pt.Program("module")

# Int8_t functions.

# TODO(adbenson): refactor this to take in arguments for better testing

program.add_func(
    "add_i8",
    (),
    pt.Int8_t,
    [
        pt.Assign(pt.Declare(pt.Int8_t, "a"), pt.Add(pt.Int8(-11), pt.Int8(-4))),
        pt.Assign(pt.Declare(pt.Int8_t, "b"), pt.Add(pt.Int8(-11), pt.Int8(0))),
        pt.Assign(pt.Declare(pt.Int8_t, "c"), pt.Add(pt.Int8(-11), pt.Int8(7))),
        pt.Assign(pt.Declare(pt.Int8_t, "d"), pt.Add(pt.Int8(0), pt.Int8(-5))),
        pt.Assign(pt.Declare(pt.Int8_t, "e"), pt.Add(pt.Int8(0), pt.Int8(0))),
        pt.Assign(pt.Declare(pt.Int8_t, "f"), pt.Add(pt.Int8(0), pt.Int8(3))),
        pt.Assign(pt.Declare(pt.Int8_t, "g"), pt.Add(pt.Int8(7), pt.Int8(-8))),
        pt.Assign(pt.Declare(pt.Int8_t, "h"), pt.Add(pt.Int8(7), pt.Int8(0))),
        pt.Assign(pt.Declare(pt.Int8_t, "i"), pt.Add(pt.Int8(7), pt.Int8(8))),
        pt.Return(
            pt.Add(
                pt.Var("a"),
                pt.Add(
                    pt.Var("b"),
                    pt.Add(
                        pt.Var("c"),
                        pt.Add(
                            pt.Var("d"),
                            pt.Add(
                                pt.Var("e"),
                                pt.Add(
                                    pt.Var("f"),
                                    pt.Add(
                                        pt.Var("g"), pt.Add(pt.Var("h"), pt.Var("i"))
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
        ),
    ],
)

# Int32_t functions.

# TODO(adbenson): refactor this to take in arguments for better testing

program.add_func(
    "add_i32",
    (),
    pt.Int32_t,
    [
        pt.Assign(pt.Declare(pt.Int32_t, "a"), pt.Add(pt.Int32(-11), pt.Int32(-4))),
        pt.Assign(pt.Declare(pt.Int32_t, "b"), pt.Add(pt.Int32(-11), pt.Int32(0))),
        pt.Assign(pt.Declare(pt.Int32_t, "c"), pt.Add(pt.Int32(-11), pt.Int32(7))),
        pt.Assign(pt.Declare(pt.Int32_t, "d"), pt.Add(pt.Int32(0), pt.Int32(-5))),
        pt.Assign(pt.Declare(pt.Int32_t, "e"), pt.Add(pt.Int32(0), pt.Int32(0))),
        pt.Assign(pt.Declare(pt.Int32_t, "f"), pt.Add(pt.Int32(0), pt.Int32(3))),
        pt.Assign(pt.Declare(pt.Int32_t, "g"), pt.Add(pt.Int32(7), pt.Int32(-8))),
        pt.Assign(pt.Declare(pt.Int32_t, "h"), pt.Add(pt.Int32(7), pt.Int32(0))),
        pt.Assign(pt.Declare(pt.Int32_t, "i"), pt.Add(pt.Int32(7), pt.Int32(8))),
        pt.Return(
            pt.Add(
                pt.Var("a"),
                pt.Add(
                    pt.Var("b"),
                    pt.Add(
                        pt.Var("c"),
                        pt.Add(
                            pt.Var("d"),
                            pt.Add(
                                pt.Var("e"),
                                pt.Add(
                                    pt.Var("f"),
                                    pt.Add(
                                        pt.Var("g"), pt.Add(pt.Var("h"), pt.Var("i"))
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
        ),
    ],
)


class ConstantsTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = program.compile()

        add_i8 = self.engine.get_function_address("add_i8")
        self.add_i8 = CFUNCTYPE(c_int8)(add_i8)

        add_i32 = self.engine.get_function_address("add_i32")
        self.add_i32 = CFUNCTYPE(c_int32)(add_i32)

    def test_add_i8(self):
        self.assertEqual(self.add_i8(), -11)

    def test_add_i32(self):
        self.assertEqual(self.add_i32(), -11)

    def test_mismatch_type_add(self):
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Add(pt.Int8(2), pt.Int32(2))),]
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Add(pt.Int32(2), pt.Int8(2))),]
            )

    def test_mismatch_type_sub(self):
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Sub(pt.Int8(2), pt.Int32(2))),]
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Sub(pt.Int32(2), pt.Int8(2))),]
            )

    def test_mismatch_type_mul(self):
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Mul(pt.Int8(2), pt.Int32(2))),]
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Mul(pt.Int32(2), pt.Int8(2))),]
            )

    def test_mismatch_type_div(self):
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Div(pt.Int8(2), pt.Int32(2))),]
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Div(pt.Int32(2), pt.Int8(2))),]
            )

    def test_mismatch_type_mod(self):
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Mod(pt.Int8(2), pt.Int32(2))),]
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, [pt.Return(pt.Mod(pt.Int32(2), pt.Int8(2))),]
            )
