from typing import cast, Callable

import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32, c_int64

program = pt.Program("module")

Pointer_Int64_t = pt.PointerType(pt.Int64_t)

# void* malloc( size_t size );
program.add_func_decl("malloc", (pt.Int64_t,), Pointer_Int64_t)
# void free( void* ptr);
program.add_func_decl("free", (Pointer_Int64_t,), ())
# void* memset ( void* ptr, int value, size_t num );
program.add_func_decl(
    "memset", (Pointer_Int64_t, pt.Int32_t, pt.Int64_t), Pointer_Int64_t
)


ptr = pt.Symbol(Pointer_Int64_t, "ptr")
val = pt.Symbol(pt.Int64_t, "val")
v32 = pt.Symbol(pt.Int32_t, "val")

program.add_func(
    "malloc_free",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(ptr, pt.Call("malloc", [pt.Int64(8)])),
            pt.Call("free", [pt.Var(ptr)]),
            pt.Return(pt.Int32(1)),
        ]
    ),
)

program.add_func(
    "malloc_memset",
    (),
    pt.Int64_t,
    pt.Block(
        [
            pt.DefineVar(ptr, pt.Call("malloc", [pt.Int64(8)])),
            pt.Assign(
                pt.Var(ptr),
                pt.Call("memset", [pt.Var(ptr), pt.Int32(0x3A), pt.Int64(8)]),
            ),
            pt.DefineVar(val, pt.Deref(pt.Var(ptr))),
            pt.Call("free", [pt.Var(ptr)]),
            pt.Return(pt.Var(val)),
        ]
    ),
)


class PointersTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        malloc_free = self.engine.get_function_address("malloc_free")
        self.malloc_free = cast(Callable[[], int], CFUNCTYPE(c_int32)(malloc_free))

        malloc_memset = self.engine.get_function_address("malloc_memset")
        self.malloc_memset = cast(Callable[[], int], CFUNCTYPE(c_int64)(malloc_memset))

    def test_malloc_free(self) -> None:
        self.assertEqual(self.malloc_free(), 1)

    def test_malloc_memset(self) -> None:
        self.assertEqual(self.malloc_memset(), 0x3A3A3A3A3A3A3A3A)

    def test_mismatch_type_deref(self) -> None:
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (), pt.Int32_t, pt.Block([pt.Return(pt.Deref(pt.Int64(123)))]),
            )
        with self.assertRaises(pt.TypeCheckError):
            pt.Program("module").add_func(
                "foo", (ptr,), (), pt.Block([pt.DefineVar(v32, pt.Deref(pt.Var(ptr))),])
            )
