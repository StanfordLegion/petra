from typing import cast, Callable

import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32, c_bool

program = pt.Program("module")

program.add_func(
    "if_else_true",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.If(
                pt.Lt(pt.Int32(0), pt.Int32(1)),
                pt.Block([pt.Return(pt.Int32(1)),]),
                pt.Block([pt.Return(pt.Int32(2))]),
            ),
            pt.Return(pt.Int32(0)),
        ]
    ),
)

program.add_func(
    "if_else_false",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.If(
                pt.Lt(pt.Int32(1), pt.Int32(0)),
                pt.Block([pt.Return(pt.Int32(1)),]),
                pt.Block([pt.Return(pt.Int32(2))]),
            ),
            pt.Return(pt.Int32(0)),
        ]
    ),
)


x = pt.Symbol(pt.Int32_t, "x")
program.add_func(
    "while_then",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(x, pt.Int32(0)),
            pt.While(
                pt.Lt(pt.Var(x), pt.Int32(10)),
                pt.Block([pt.Assign(pt.Var(x), pt.Add(pt.Var(x), pt.Int32(1)),),]),
            ),
            pt.Return(pt.Var(x)),
        ]
    ),
)


class ConditionalsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        # If statement

        if_else_true = self.engine.get_function_address("if_else_true")
        self.if_else_true = cast(Callable[[], int], CFUNCTYPE(c_int32)(if_else_true))

        if_else_false = self.engine.get_function_address("if_else_false")
        self.if_else_false = cast(Callable[[], int], CFUNCTYPE(c_int32)(if_else_false))

        # While loop

        while_then = self.engine.get_function_address("while_then")
        self.while_then = cast(Callable[[], int], CFUNCTYPE(c_int32)(while_then))

    def test_if_then(self) -> None:
        self.assertEqual(self.if_else_true(), 1)
        self.assertEqual(self.if_else_false(), 2)

    def test_while_then(self) -> None:
        self.assertEqual(self.while_then(), 10)
