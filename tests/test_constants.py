from typing import cast, Callable

import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int8, c_int16, c_int32, c_int64

program = pt.Program("module")

# Int8_t functions.

program.add_func("return_m2_i8", (), pt.Int8_t, pt.Block([pt.Return(pt.Int8(-2))]))

program.add_func("return_0_i8", (), pt.Int8_t, pt.Block([pt.Return(pt.Int8(0))]))

program.add_func("return_2_i8", (), pt.Int8_t, pt.Block([pt.Return(pt.Int8(2))]))

# Int16_t functions.

program.add_func("return_m2_i16", (), pt.Int16_t, pt.Block([pt.Return(pt.Int16(-2))]))

program.add_func("return_0_i16", (), pt.Int16_t, pt.Block([pt.Return(pt.Int16(0))]))

program.add_func("return_2_i16", (), pt.Int16_t, pt.Block([pt.Return(pt.Int16(2))]))

# Int32_t functions.

program.add_func("return_m2_i32", (), pt.Int32_t, pt.Block([pt.Return(pt.Int32(-2))]))

program.add_func("return_0_i32", (), pt.Int32_t, pt.Block([pt.Return(pt.Int32(0))]))

program.add_func("return_2_i32", (), pt.Int32_t, pt.Block([pt.Return(pt.Int32(2))]))

# Int64_t functions.

program.add_func("return_m2_i64", (), pt.Int64_t, pt.Block([pt.Return(pt.Int64(-2))]))

program.add_func("return_0_i64", (), pt.Int64_t, pt.Block([pt.Return(pt.Int64(0))]))

program.add_func("return_2_i64", (), pt.Int64_t, pt.Block([pt.Return(pt.Int64(2))]))


class ConstantsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        # Int8_t

        return_m2_i8 = self.engine.get_function_address("return_m2_i8")
        self.return_m2_i8 = cast(Callable[[], int], CFUNCTYPE(c_int8)(return_m2_i8))

        return_0_i8 = self.engine.get_function_address("return_0_i8")
        self.return_0_i8 = cast(Callable[[], int], CFUNCTYPE(c_int8)(return_0_i8))

        return_2_i8 = self.engine.get_function_address("return_2_i8")
        self.return_2_i8 = cast(Callable[[], int], CFUNCTYPE(c_int8)(return_2_i8))

        # Int16_t

        return_m2_i16 = self.engine.get_function_address("return_m2_i16")
        self.return_m2_i16 = cast(Callable[[], int], CFUNCTYPE(c_int16)(return_m2_i16))

        return_0_i16 = self.engine.get_function_address("return_0_i16")
        self.return_0_i16 = cast(Callable[[], int], CFUNCTYPE(c_int16)(return_0_i16))

        return_2_i16 = self.engine.get_function_address("return_2_i16")
        self.return_2_i16 = cast(Callable[[], int], CFUNCTYPE(c_int16)(return_2_i16))

        # Int32_t

        return_m2_i32 = self.engine.get_function_address("return_m2_i32")
        self.return_m2_i32 = cast(Callable[[], int], CFUNCTYPE(c_int32)(return_m2_i32))

        return_0_i32 = self.engine.get_function_address("return_0_i32")
        self.return_0_i32 = cast(Callable[[], int], CFUNCTYPE(c_int32)(return_0_i32))

        return_2_i32 = self.engine.get_function_address("return_2_i32")
        self.return_2_i32 = cast(Callable[[], int], CFUNCTYPE(c_int32)(return_2_i32))

        # Int64_t

        return_m2_i64 = self.engine.get_function_address("return_m2_i64")
        self.return_m2_i64 = cast(Callable[[], int], CFUNCTYPE(c_int64)(return_m2_i64))

        return_0_i64 = self.engine.get_function_address("return_0_i64")
        self.return_0_i64 = cast(Callable[[], int], CFUNCTYPE(c_int64)(return_0_i64))

        return_2_i64 = self.engine.get_function_address("return_2_i64")
        self.return_2_i64 = cast(Callable[[], int], CFUNCTYPE(c_int64)(return_2_i64))

    # Int8_t

    def test_return_m2_i8(self) -> None:
        self.assertEqual(self.return_m2_i8(), -2)

    def test_return_0_i8(self) -> None:
        self.assertEqual(self.return_0_i8(), 0)

    def test_return_2_i8(self) -> None:
        self.assertEqual(self.return_2_i8(), 2)

    # Int16_t

    def test_return_m2_i16(self) -> None:
        self.assertEqual(self.return_m2_i16(), -2)

    def test_return_0_i16(self) -> None:
        self.assertEqual(self.return_0_i16(), 0)

    def test_return_2_i16(self) -> None:
        self.assertEqual(self.return_2_i16(), 2)

    # Int32_t

    def test_return_m2_i32(self) -> None:
        self.assertEqual(self.return_m2_i32(), -2)

    def test_return_0_i32(self) -> None:
        self.assertEqual(self.return_0_i32(), 0)

    def test_return_2_i32(self) -> None:
        self.assertEqual(self.return_2_i32(), 2)

    # Int64_t

    def test_return_m2_i64(self) -> None:
        self.assertEqual(self.return_m2_i64(), -2)

    def test_return_0_i64(self) -> None:
        self.assertEqual(self.return_0_i64(), 0)

    def test_return_2_i64(self) -> None:
        self.assertEqual(self.return_2_i64(), 2)

    # Int8_t

    def test_below_bounds_i8(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Int8(-129)

    def test_above_bounds_i8(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Int8(128)

    # Int16_t

    def test_below_bounds_i16(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Int16(-(2 ** 15) - 1)

    def test_above_bounds_i16(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Int16(2 ** 15)

    # Int32_t

    def test_below_bounds_i32(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Int32(-(2 ** 31) - 1)

    def test_above_bounds_i32(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Int32(2 ** 31)

    # Int64_t

    def test_below_bounds_i64(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Int64(-(2 ** 63) - 1)

    def test_above_bounds_i64(self) -> None:
        with self.assertRaises(pt.ValidateError):
            pt.Int64(2 ** 63)
