import petra as pt

program = pt.Program("module")

program.add_func(
    "collatz",
    (pt.Declare(pt.Int32_t, "n"),),
    pt.Int32_t,
    pt.Block(
        [
            pt.If(
                pt.Eq(pt.Var("n"), pt.Int32(1)),
                pt.Block([pt.Return(pt.Int32(0))]),
                pt.Block([]),
            ),
            pt.If(
                pt.Eq(pt.Mod(pt.Var("n"), pt.Int32(2)), pt.Int32(0)),
                pt.Block([pt.Assign(pt.Var("n"), pt.Div(pt.Var("n"), pt.Int32(2)))]),
                pt.Block(
                    [
                        pt.Assign(
                            pt.Var("n"),
                            pt.Add(pt.Mul(pt.Int32(3), pt.Var("n")), pt.Int32(1)),
                        ),
                    ]
                ),
            ),
            pt.Return(pt.Add(pt.Int32(1), pt.Call("collatz", [pt.Var("n")]))),
        ]
    ),
)

program.save_object("collatz.py.o")
