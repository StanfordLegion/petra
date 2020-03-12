import petra as pt

program = pt.Program("module")

program.add_func_decl("sqrtf", (pt.Float32_t,), pt.Float32_t)

program.add_func(
    "call_sqrtf",
    (pt.Declare(pt.Float32_t, "x"),),
    pt.Float32_t,
    pt.Block([pt.Return(pt.Call("sqrtf", [pt.Var("x")]))]),
)

print(program.to_llvm())
