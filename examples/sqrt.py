import petra as pt

program = pt.Program("module")

program.add_func_decl("sqrtf", (pt.Float_t,), pt.Float_t)

program.add_func(
    "call_sqrtf",
    (pt.Declare(pt.Float_t, "x"),),
    pt.Float_t,
    pt.Block([pt.Return(pt.Call("sqrtf", [pt.Var("x")]))]),
)

print(program.to_llvm())
