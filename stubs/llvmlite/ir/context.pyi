from . import types as types
from typing import Any

class Context:
    scope: Any = ...
    identified_types: Any = ...
    def __init__(self) -> None: ...
    def get_identified_type(self, name: Any): ...

global_context: Any
