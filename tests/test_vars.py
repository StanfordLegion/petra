import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32

program = pt.Program("module")

program.add_func(
    "return_temp",
    (),
    pt.Int32_t,
    pt.Block(
        [pt.Assign(pt.Declare(pt.Int32_t, "x"), pt.Int32(2)), pt.Return(pt.Var("x"))]
    ),
)

program.add_func(
    "return_shuffle_temp",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.Assign(pt.Declare(pt.Int32_t, "x"), pt.Int32(2)),
            pt.Assign(pt.Declare(pt.Int32_t, "y"), pt.Var("x")),
            pt.Return(pt.Var("y")),
        ]
    ),
)

program.add_func(
    "temp_unused",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.Assign(pt.Declare(pt.Int32_t, "x"), pt.Int32(500)),
            pt.Assign(pt.Declare(pt.Int32_t, "y"), pt.Var("x")),
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
            pt.Assign(pt.Declare(pt.Int32_t, "x"), pt.Int32(2)),
            pt.Assign(pt.Declare(pt.Int32_t, "y"), pt.Var("x")),
            pt.Return(pt.Var("x")),
        ]
    ),
)


class VarsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        return_temp = self.engine.get_function_address("return_temp")
        self.return_temp = CFUNCTYPE(c_int32)(return_temp)

        return_shuffle_temp = self.engine.get_function_address("return_shuffle_temp")
        self.return_shuffle_temp = CFUNCTYPE(c_int32)(return_shuffle_temp)

        temp_unused = self.engine.get_function_address("temp_unused")
        self.temp_unused = CFUNCTYPE(c_int32)(temp_unused)

        return_temp_unused = self.engine.get_function_address("return_temp_unused")
        self.return_temp_unused = CFUNCTYPE(c_int32)(return_temp_unused)

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
            pt.Var("_")
        with self.assertRaises(pt.ValidateError):
            pt.Var("_a")
        with self.assertRaises(pt.ValidateError):
            pt.Var("A")
        with self.assertRaises(pt.ValidateError):
            pt.Var("Aa")
        with self.assertRaises(pt.ValidateError):
            pt.Var("0")
        with self.assertRaises(pt.ValidateError):
            pt.Var("0a")
        pt.Var("a")
        pt.Var("aa")

    def test_variable_name_contains_forbidden(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Var("a*")
        with self.assertRaises(pt.ValidateError):
            pt.Var("a-a")
        with self.assertRaises(pt.ValidateError):
            pt.Var("a+a")
        with self.assertRaises(pt.ValidateError):
            pt.Var("a🤔")
        with self.assertRaises(pt.ValidateError):
            pt.Var("a猫")
        with self.assertRaises(pt.ValidateError):
            pt.Var("a ")
        pt.Var("aBCD")
        pt.Var("a_B_02")
        pt.Var("a554")

    def test_declare_undeclared_variable(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block(
                    [
                        pt.Assign(pt.Declare(pt.Int32_t, "x"), pt.Var("x")),
                        pt.Return(pt.Int32(2)),
                    ]
                ),
            )

    def test_assign_undeclared_variable(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block(
                    [pt.Assign(pt.Var("x"), pt.Int32(500)), pt.Return(pt.Int32(2)),]
                ),
            )

    def test_return_undeclared_variable(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, pt.Block([pt.Return(pt.Var("x"))])
            )

    def test_redeclared_variable(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block(
                    [
                        pt.Assign(pt.Declare(pt.Int32_t, "x"), pt.Int32(2)),
                        pt.Assign(pt.Declare(pt.Int32_t, "x"), pt.Int32(3)),
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
                pt.Block(
                    [
                        pt.Assign(pt.Declare(pt.Int8_t, "x"), pt.Int32(2)),
                        pt.Return(pt.Int32(2)),
                    ]
                ),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo",
                (),
                pt.Int32_t,
                pt.Block(
                    [
                        pt.Assign(pt.Declare(pt.Int32_t, "x"), pt.Int8(2)),
                        pt.Return(pt.Int32(2)),
                    ]
                ),
            )
