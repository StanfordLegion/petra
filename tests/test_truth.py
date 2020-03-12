from typing import cast, Callable

import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_bool, c_int8

program = pt.Program("module")

x, y = pt.Symbol(pt.Int8_t, "x"), pt.Symbol(pt.Int8_t, "y")
z, w = pt.Symbol(pt.Bool_t, "z"), pt.Symbol(pt.Bool_t, "w")

program.add_func(
    "lt", (x, y), pt.Bool_t, pt.Block([pt.Return(pt.Lt(pt.Var(x), pt.Var(y)))]),
)

program.add_func(
    "lte", (x, y), pt.Bool_t, pt.Block([pt.Return(pt.Lte(pt.Var(x), pt.Var(y)))]),
)

program.add_func(
    "gt", (x, y), pt.Bool_t, pt.Block([pt.Return(pt.Gt(pt.Var(x), pt.Var(y)))]),
)

program.add_func(
    "gte", (x, y), pt.Bool_t, pt.Block([pt.Return(pt.Gte(pt.Var(x), pt.Var(y)))]),
)

program.add_func(
    "eq", (x, y), pt.Bool_t, pt.Block([pt.Return(pt.Eq(pt.Var(x), pt.Var(y)))]),
)

program.add_func(
    "eqb", (z, w), pt.Bool_t, pt.Block([pt.Return(pt.Eq(pt.Var(z), pt.Var(w)))]),
)

program.add_func(
    "neq", (x, y), pt.Bool_t, pt.Block([pt.Return(pt.Neq(pt.Var(x), pt.Var(y)))]),
)

program.add_func(
    "neqb", (z, w), pt.Bool_t, pt.Block([pt.Return(pt.Neq(pt.Var(z), pt.Var(w)))]),
)

program.add_func(
    "and_", (z, w), pt.Bool_t, pt.Block([pt.Return(pt.And(pt.Var(z), pt.Var(w)))]),
)

program.add_func(
    "or_", (z, w), pt.Bool_t, pt.Block([pt.Return(pt.Or(pt.Var(z), pt.Var(w)))]),
)

program.add_func(
    "not_", (z,), pt.Bool_t, pt.Block([pt.Return(pt.Not(pt.Var(z)))]),
)


class TruthTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        lt = self.engine.get_function_address("lt")
        self.lt = cast(
            Callable[[int, int], bool], CFUNCTYPE(c_bool, c_int8, c_int8)(lt)
        )

        lte = self.engine.get_function_address("lte")
        self.lte = cast(
            Callable[[int, int], bool], CFUNCTYPE(c_bool, c_int8, c_int8)(lte)
        )

        gt = self.engine.get_function_address("gt")
        self.gt = cast(
            Callable[[int, int], bool], CFUNCTYPE(c_bool, c_int8, c_int8)(gt)
        )

        gte = self.engine.get_function_address("gte")
        self.gte = cast(
            Callable[[int, int], bool], CFUNCTYPE(c_bool, c_int8, c_int8)(gte)
        )

        eq = self.engine.get_function_address("eq")
        self.eq = cast(
            Callable[[int, int], bool], CFUNCTYPE(c_bool, c_int8, c_int8)(eq)
        )

        eqb = self.engine.get_function_address("eqb")
        self.eqb = cast(
            Callable[[bool, bool], bool], CFUNCTYPE(c_bool, c_bool, c_bool)(eqb)
        )

        neq = self.engine.get_function_address("neq")
        self.neq = cast(
            Callable[[int, int], bool], CFUNCTYPE(c_bool, c_int8, c_int8)(neq)
        )

        neqb = self.engine.get_function_address("neqb")
        self.neqb = cast(
            Callable[[bool, bool], bool], CFUNCTYPE(c_bool, c_bool, c_bool)(neqb)
        )

        and_ = self.engine.get_function_address("and_")
        self.and_ = cast(
            Callable[[bool, bool], bool], CFUNCTYPE(c_bool, c_bool, c_bool)(and_)
        )

        or_ = self.engine.get_function_address("or_")
        self.or_ = cast(
            Callable[[bool, bool], bool], CFUNCTYPE(c_bool, c_bool, c_bool)(or_)
        )

        not_ = self.engine.get_function_address("not_")
        self.not_ = cast(Callable[[bool], bool], CFUNCTYPE(c_bool, c_bool)(not_))

    def test_lt(self) -> None:
        self.assertFalse(self.lt(0, 0))
        self.assertTrue(self.lt(0, 3))
        self.assertFalse(self.lt(3, 0))
        self.assertFalse(self.lt(0, -3))
        self.assertTrue(self.lt(-3, 0))
        self.assertTrue(self.lt(1, 3))
        self.assertFalse(self.lt(3, 1))
        self.assertFalse(self.lt(3, 3))
        self.assertTrue(self.lt(-1, 3))
        self.assertFalse(self.lt(3, -1))
        self.assertFalse(self.lt(-1, -3))
        self.assertTrue(self.lt(-3, -1))
        self.assertFalse(self.lt(-3, -3))

    def test_lte(self) -> None:
        self.assertTrue(self.lte(0, 0))
        self.assertTrue(self.lte(0, 3))
        self.assertFalse(self.lte(3, 0))
        self.assertFalse(self.lte(0, -3))
        self.assertTrue(self.lte(-3, 0))
        self.assertTrue(self.lte(1, 3))
        self.assertFalse(self.lte(3, 1))
        self.assertTrue(self.lte(3, 3))
        self.assertTrue(self.lte(-1, 3))
        self.assertFalse(self.lte(3, -1))
        self.assertFalse(self.lte(-1, -3))
        self.assertTrue(self.lte(-3, -1))
        self.assertTrue(self.lte(-3, -3))

    def test_gt(self) -> None:
        self.assertFalse(self.gt(0, 0))
        self.assertFalse(self.gt(0, 3))
        self.assertTrue(self.gt(3, 0))
        self.assertTrue(self.gt(0, -3))
        self.assertFalse(self.gt(-3, 0))
        self.assertFalse(self.gt(1, 3))
        self.assertTrue(self.gt(3, 1))
        self.assertFalse(self.gt(3, 3))
        self.assertFalse(self.gt(-1, 3))
        self.assertTrue(self.gt(3, -1))
        self.assertTrue(self.gt(-1, -3))
        self.assertFalse(self.gt(-3, -1))
        self.assertFalse(self.gt(-3, -3))

    def test_gte(self) -> None:
        self.assertTrue(self.gte(0, 0))
        self.assertFalse(self.gte(0, 3))
        self.assertTrue(self.gte(3, 0))
        self.assertTrue(self.gte(0, -3))
        self.assertFalse(self.gte(-3, 0))
        self.assertFalse(self.gte(1, 3))
        self.assertTrue(self.gte(3, 1))
        self.assertTrue(self.gte(3, 3))
        self.assertFalse(self.gte(-1, 3))
        self.assertTrue(self.gte(3, -1))
        self.assertTrue(self.gte(-1, -3))
        self.assertFalse(self.gte(-3, -1))
        self.assertTrue(self.gte(-3, -3))

    def test_eq(self) -> None:
        self.assertTrue(self.eq(0, 0))
        self.assertFalse(self.eq(0, 3))
        self.assertFalse(self.eq(3, 0))
        self.assertFalse(self.eq(0, -3))
        self.assertFalse(self.eq(-3, 0))
        self.assertFalse(self.eq(1, 3))
        self.assertFalse(self.eq(3, 1))
        self.assertTrue(self.eq(3, 3))
        self.assertFalse(self.eq(-1, 3))
        self.assertFalse(self.eq(3, -1))
        self.assertFalse(self.eq(-1, -3))
        self.assertFalse(self.eq(-3, -1))
        self.assertTrue(self.eq(-3, -3))

    def test_eqb(self) -> None:
        self.assertTrue(self.eqb(True, True))
        self.assertFalse(self.eqb(True, False))
        self.assertFalse(self.eqb(False, True))
        self.assertTrue(self.eqb(False, False))

    def test_neq(self) -> None:
        self.assertFalse(self.neq(0, 0))
        self.assertTrue(self.neq(0, 3))
        self.assertTrue(self.neq(3, 0))
        self.assertTrue(self.neq(0, -3))
        self.assertTrue(self.neq(-3, 0))
        self.assertTrue(self.neq(1, 3))
        self.assertTrue(self.neq(3, 1))
        self.assertFalse(self.neq(3, 3))
        self.assertTrue(self.neq(-1, 3))
        self.assertTrue(self.neq(3, -1))
        self.assertTrue(self.neq(-1, -3))
        self.assertTrue(self.neq(-3, -1))
        self.assertFalse(self.neq(-3, -3))

    def test_neqb(self) -> None:
        self.assertFalse(self.neqb(True, True))
        self.assertTrue(self.neqb(True, False))
        self.assertTrue(self.neqb(False, True))
        self.assertFalse(self.neqb(False, False))

    def test_and(self) -> None:
        self.assertTrue(self.and_(True, True))
        self.assertFalse(self.and_(True, False))
        self.assertFalse(self.and_(False, True))
        self.assertFalse(self.and_(False, False))

    def test_or(self) -> None:
        self.assertTrue(self.or_(True, True))
        self.assertTrue(self.or_(True, False))
        self.assertTrue(self.or_(False, True))
        self.assertFalse(self.or_(False, False))

    def test_not(self) -> None:
        self.assertTrue(self.not_(False))
        self.assertFalse(self.not_(True))
