from . import ffi as ffi
from .module import parse_assembly as parse_assembly
from llvmlite import ir as ir
from typing import Any, Optional

def get_function_cfg(func: Any, show_inst: bool = ...): ...
def view_dot_graph(graph: Any, filename: Optional[Any] = ..., view: bool = ...): ...
