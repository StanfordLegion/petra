import petra as pt

program = pt.Program("module")

program.add_func_decl("sqrtf", (pt.Float32_t,), pt.Float32_t)

x = pt.Symbol(pt.Float32_t, "x")

program.add_func(
    "call_sqrtf",
    (x,),
    pt.Float32_t,
    pt.Block([pt.Return(pt.Call("sqrtf", [pt.Var(x)]))]),
)

program.save_object("sqrt.py.o")
