from . import types as types
from ._utils import _HasMetadata, _StrCaching, _StringReferenceCaching
from typing import Any

class _ConstOpMixin:
    def bitcast(self, typ: Any): ...
    def inttoptr(self, typ: Any): ...
    def gep(self, indices: Any): ...

class Value: ...

class _Undefined:
    def __new__(cls): ...

Undefined: Any

class Constant(_StrCaching, _StringReferenceCaching, _ConstOpMixin, Value):
    type: Any = ...
    constant: Any = ...
    def __init__(self, typ: Any, constant: Any) -> None: ...
    @classmethod
    def literal_array(cls, elems: Any): ...
    @classmethod
    def literal_struct(cls, elems: Any): ...
    @property
    def addrspace(self): ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...

class FormattedConstant(Constant):
    def __init__(self, typ: Any, constant: Any) -> None: ...

class NamedValue(_StrCaching, _StringReferenceCaching, Value):
    name_prefix: str = ...
    deduplicate_name: bool = ...
    parent: Any = ...
    type: Any = ...
    def __init__(self, parent: Any, type: Any, name: Any) -> None: ...
    def descr(self, buf: Any) -> None: ...
    name: Any = ...
    @property
    def function_type(self): ...

class MetaDataString(NamedValue):
    string: Any = ...
    def __init__(self, parent: Any, string: Any) -> None: ...
    def descr(self, buf: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...

class MetaDataArgument(_StrCaching, _StringReferenceCaching, Value):
    type: Any = ...
    wrapped_value: Any = ...
    def __init__(self, value: Any) -> None: ...

class NamedMetaData:
    parent: Any = ...
    operands: Any = ...
    def __init__(self, parent: Any) -> None: ...
    def add(self, md: Any) -> None: ...

class MDValue(NamedValue):
    name_prefix: str = ...
    operands: Any = ...
    def __init__(self, parent: Any, values: Any, name: Any) -> None: ...
    def descr(self, buf: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...

class DIToken:
    value: Any = ...
    def __init__(self, value: Any) -> None: ...

class DIValue(NamedValue):
    name_prefix: str = ...
    is_distinct: Any = ...
    kind: Any = ...
    operands: Any = ...
    def __init__(
        self, parent: Any, is_distinct: Any, kind: Any, operands: Any, name: Any
    ) -> None: ...
    def descr(self, buf: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...

class GlobalValue(NamedValue, _ConstOpMixin):
    name_prefix: str = ...
    deduplicate_name: bool = ...
    linkage: str = ...
    storage_class: str = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class GlobalVariable(GlobalValue):
    value_type: Any = ...
    initializer: Any = ...
    unnamed_addr: bool = ...
    global_constant: bool = ...
    addrspace: Any = ...
    align: Any = ...
    def __init__(
        self, module: Any, typ: Any, name: Any, addrspace: int = ...
    ) -> None: ...
    def descr(self, buf: Any) -> None: ...

class AttributeSet(set):
    def __init__(self, args: Any = ...) -> None: ...
    def add(self, name: Any): ...
    def __iter__(self) -> Any: ...

class FunctionAttributes(AttributeSet):
    def __init__(self, args: Any = ...) -> None: ...
    @property
    def alignstack(self): ...
    @alignstack.setter
    def alignstack(self, val: Any) -> None: ...
    @property
    def personality(self): ...
    @personality.setter
    def personality(self, val: Any) -> None: ...

class Function(GlobalValue, _HasMetadata):
    ftype: Any = ...
    scope: Any = ...
    blocks: List[Block] = ...
    attributes: Any = ...
    args: Tuple[Argument, ...] = ...
    return_value: Any = ...
    calling_convention: str = ...
    metadata: Any = ...
    def __init__(self, module: Any, ftype: Any, name: Any) -> None: ...
    @property
    def module(self): ...
    @property
    def entry_basic_block(self) -> Block: ...
    @property
    def basic_blocks(self) -> List[Block]: ...
    def append_basic_block(self, name: str = ...) -> Block: ...
    def insert_basic_block(self, before: Any, name: str = ...) -> Block: ...
    def descr_prototype(self, buf: Any) -> None: ...
    def descr_body(self, buf: Any) -> None: ...
    def descr(self, buf: Any) -> None: ...
    @property
    def is_declaration(self): ...

class ArgumentAttributes(AttributeSet):
    def __init__(self, args: Any = ...) -> None: ...
    @property
    def align(self): ...
    @align.setter
    def align(self, val: Any) -> None: ...
    @property
    def dereferenceable(self): ...
    @dereferenceable.setter
    def dereferenceable(self, val: Any) -> None: ...
    @property
    def dereferenceable_or_null(self): ...
    @dereferenceable_or_null.setter
    def dereferenceable_or_null(self, val: Any) -> None: ...

class _BaseArgument(NamedValue):
    parent: Any = ...
    attributes: Any = ...
    def __init__(self, parent: Any, typ: Any, name: str = ...) -> None: ...
    def add_attribute(self, attr: Any) -> None: ...

class Argument(_BaseArgument): ...
class ReturnValue(_BaseArgument): ...

class Block(NamedValue):
    scope: Any = ...
    instructions: Any = ...
    terminator: Any = ...
    def __init__(self, parent: Any, name: str = ...) -> None: ...
    @property
    def is_terminated(self): ...
    @property
    def function(self): ...
    @property
    def module(self): ...
    def descr(self, buf: Any) -> None: ...
    def replace(self, old: Any, new: Any) -> None: ...

class BlockAddress(Value):
    type: Any = ...
    function: Any = ...
    basic_block: Any = ...
    def __init__(self, function: Any, basic_block: Any) -> None: ...
    def get_reference(self): ...
