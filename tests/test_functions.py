import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32

program = pt.Program("module")

program.add_func("return_2", (), pt.Int32_t, pt.Block([pt.Return(pt.Int32(2))]))

program.add_func(
    "call_return_2", (), pt.Int32_t, pt.Block([pt.Return(pt.Call("return_2", []))])
)

program.add_func(
    "call_return_2_discard",
    (),
    pt.Int32_t,
    pt.Block([pt.Call("return_2", []), pt.Return(pt.Int32(3))]),
)

program.add_func(
    "iden",
    (pt.Declare(pt.Int32_t, "x"),),
    pt.Int32_t,
    pt.Block([pt.Return(pt.Var("x"))]),
)

program.add_func(
    "sum",
    (pt.Declare(pt.Int32_t, "x"), pt.Declare(pt.Int32_t, "y")),
    pt.Int32_t,
    pt.Block([pt.Return(pt.Add(pt.Var("x"), pt.Var("y")))]),
)


class FunctionsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        return_2 = self.engine.get_function_address("return_2")
        self.return_2 = CFUNCTYPE(c_int32)(return_2)

        call_return_2 = self.engine.get_function_address("call_return_2")
        self.call_return_2 = CFUNCTYPE(c_int32)(call_return_2)

        call_return_2_discard = self.engine.get_function_address(
            "call_return_2_discard"
        )
        self.call_return_2_discard = CFUNCTYPE(c_int32)(call_return_2_discard)

        iden = self.engine.get_function_address("iden")
        self.iden = CFUNCTYPE(c_int32, c_int32)(iden)

        psum = self.engine.get_function_address("sum")
        self.psum = CFUNCTYPE(c_int32, c_int32, c_int32)(psum)

    def test_call_return_2(self) -> None:
        self.assertEqual(self.return_2(), 2)
        self.assertEqual(self.call_return_2(), 2)

    def test_call_return_2_discard(self) -> None:
        self.assertEqual(self.call_return_2_discard(), 3)

    def test_call_iden(self) -> None:
        for i in range(-3, 3):
            self.assertEqual(self.iden(i), i)

    def test_call_sum(self) -> None:
        for i in range(-5, 5):
            for j in range(-5, 5):
                self.assertEqual(self.psum(i, j), i + j)

    def test_return_call_nothing_for_int32_t(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "nothing", (), (), pt.Block([pt.Return(())])
            ).add_func(
                "call_nothing",
                (),
                pt.Int32_t,
                pt.Block([pt.Return(pt.Call("nothing", []))]),
            )
