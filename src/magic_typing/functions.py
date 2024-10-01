from dataclasses import dataclass
from types import UnionType, GenericAlias
from typing import TypeVar

TypeAnnotation = UnionType | GenericAlias | type | TypeVar

@dataclass
class FunctionInfo:
    is_strict: bool
    argument_types: list[TypeAnnotation]
    return_type: TypeAnnotation

def get_function_info(name: str) -> FunctionInfo:
    raise NotImplementedError

# Since modules are only loaded once, we can use a module-level variable to cache
# information on already seen functions.
FUNCTIONS: dict[str, FunctionInfo] = {}
