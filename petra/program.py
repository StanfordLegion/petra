"""
This file defines Petra programs.
"""

from __future__ import annotations  # necessary to avoid forward declarations
from llvmlite import ir, binding
from typing import Dict, List, Tuple

from .block import Block
from .codegen import convert_func_type
from .function import Ftypein, Ftypeout, Function
from .statement import Declare, Statement


class Program(object):
    """
    A Petra program. Petra programs can be codegen'ed to LLVM.
    """

    llvm_initialized: bool = False

    def __init__(self, name: str):
        self.module = ir.Module(name=name)
        self.functypes: Dict[str, Tuple[Ftypein, Ftypeout]] = dict()
        self.funcs: Dict[str, ir.Function] = dict()

    def add_func_decl(self, name: str, t_in: Ftypein, t_out: Ftypeout) -> Program:
        if name in self.functypes:
            raise Exception("Function %s already exists in program." % name)
        self.functypes[name] = (t_in, t_out)
        self.funcs[name] = ir.Function(
            self.module, convert_func_type(t_in, t_out), name
        )
        return self

    def add_func(
        self, name: str, args: Tuple[Declare, ...], t_out: Ftypeout, block: Block,
    ) -> Program:
        if name in self.functypes:
            raise Exception("Function %s already exists in program." % name)
        t_in = tuple(arg.t for arg in args)
        self.functypes[name] = (t_in, t_out)
        self.funcs[name] = ir.Function(
            self.module, convert_func_type(t_in, t_out), name
        )
        func = Function(name, args, t_out, block, self.functypes)
        func.codegen(self.module, self.funcs)
        return self

    def to_llvm(self) -> str:
        return str(self.module)

    def save_object(self, filename: str) -> None:
        if not self.llvm_initialized:
            self.llvm_initialized = True
            binding.initialize()
            binding.initialize_native_target()
            binding.initialize_native_asmprinter()
        # FIXME: Not sure why MyPy can't type check this, maybe a bug
        target = binding.Target.from_default_triple()  # type: ignore
        target_machine = target.create_target_machine()
        backing_mod = binding.parse_assembly(self.to_llvm())
        with open(filename, "wb") as f:
            f.write(target_machine.emit_object(backing_mod))

    def compile(self) -> binding.ExecutionEngine:
        if not self.llvm_initialized:
            self.llvm_initialized = True
            binding.initialize()
            binding.initialize_native_target()
            binding.initialize_native_asmprinter()
        # FIXME: Not sure why MyPy can't type check this, maybe a bug
        target = binding.Target.from_default_triple()  # type: ignore
        target_machine = target.create_target_machine()
        backing_mod = binding.parse_assembly(self.to_llvm())
        engine = binding.create_mcjit_compiler(backing_mod, target_machine)
        engine.finalize_object()
        engine.run_static_constructors()
        return engine
