from . import ffi as ffi, object_file as object_file, targets as targets
from ctypes import Structure
from typing import Any, Optional

def create_mcjit_compiler(module: Any, target_machine: Any) -> ExecutionEngine: ...
def check_jit_execution() -> None: ...

class ExecutionEngine(ffi.ObjectRef):
    def __init__(self, ptr: Any, module: Any) -> None: ...
    def get_function_address(self, name: Any) -> int: ...
    def get_global_value_address(self, name: Any): ...
    def add_global_mapping(self, gv: Any, addr: Any) -> None: ...
    def add_module(self, module: Any) -> None: ...
    def finalize_object(self) -> None: ...
    def run_static_constructors(self) -> None: ...
    def run_static_destructors(self) -> None: ...
    def remove_module(self, module: Any) -> None: ...
    @property
    def target_data(self): ...
    def enable_jit_events(self): ...
    def add_object_file(self, obj_file: Any) -> None: ...
    def set_object_cache(
        self, notify_func: Optional[Any] = ..., getbuffer_func: Optional[Any] = ...
    ) -> None: ...

class _ObjectCacheRef(ffi.ObjectRef):
    def __init__(self, obj: Any) -> None: ...

class _ObjectCacheData(Structure): ...
