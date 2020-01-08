import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int8, c_int32

program = pt.Program("module")

# Int8_t functions.

program.add_func("return_m2_i8", (), pt.Int8_t, [pt.Return(pt.Int8(-2)),])

program.add_func("return_0_i8", (), pt.Int8_t, [pt.Return(pt.Int8(0)),])

program.add_func("return_2_i8", (), pt.Int8_t, [pt.Return(pt.Int8(2)),])

# Int32_t functions.

program.add_func("return_m2_i32", (), pt.Int32_t, [pt.Return(pt.Int32(-2)),])

program.add_func("return_0_i32", (), pt.Int32_t, [pt.Return(pt.Int32(0)),])

program.add_func("return_2_i32", (), pt.Int32_t, [pt.Return(pt.Int32(2)),])


class ConstantsTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = program.compile()

        return_m2_i8 = self.engine.get_function_address("return_m2_i8")
        self.return_m2_i8 = CFUNCTYPE(c_int8)(return_m2_i8)

        return_0_i8 = self.engine.get_function_address("return_0_i8")
        self.return_0_i8 = CFUNCTYPE(c_int8)(return_0_i8)

        return_2_i8 = self.engine.get_function_address("return_2_i8")
        self.return_2_i8 = CFUNCTYPE(c_int8)(return_2_i8)

        return_m2_i32 = self.engine.get_function_address("return_m2_i32")
        self.return_m2_i32 = CFUNCTYPE(c_int32)(return_m2_i32)

        return_0_i32 = self.engine.get_function_address("return_0_i32")
        self.return_0_i32 = CFUNCTYPE(c_int32)(return_0_i32)

        return_2_i32 = self.engine.get_function_address("return_2_i32")
        self.return_2_i32 = CFUNCTYPE(c_int32)(return_2_i32)

    def test_return_m2_i8(self):
        self.assertEqual(self.return_m2_i8(), -2)

    def test_return_0_i8(self):
        self.assertEqual(self.return_0_i8(), 0)

    def test_return_2_i8(self):
        self.assertEqual(self.return_2_i8(), 2)

    def test_return_m2_i32(self):
        self.assertEqual(self.return_m2_i32(), -2)

    def test_return_0_i32(self):
        self.assertEqual(self.return_0_i32(), 0)

    def test_return_2_i32(self):
        self.assertEqual(self.return_2_i32(), 2)

    def test_below_bounds_i8(self):
        with self.assertRaises(pt.StaticException):
            pt.Int8(-129)

    def test_above_bounds_i8(self):
        with self.assertRaises(pt.StaticException):
            pt.Int8(128)

    def test_below_bounds_i32(self):
        with self.assertRaises(pt.StaticException):
            pt.Int8(-(2 ** 31) - 1)

    def test_above_bounds_i32(self):
        with self.assertRaises(pt.StaticException):
            pt.Int8(2 ** 31)
