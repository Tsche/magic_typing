from ast import Assert, Attribute, Call, Constant, FormattedValue, If, JoinedStr, Name, Tuple
import ast
from typing import Iterable

def type_check(variable: str, type_:  Tuple | Name) -> Call:
    return Call(func=Name("isinstance"), args=[Name(variable), type_], keywords=[])

def assert_type(variable: str, type_: str | Iterable[str]) -> Assert:
    types: Name | Tuple = (Name(type_)
                           if isinstance(type_, str)
                           else Tuple(elts=[Name(variant) for variant in type_]))

    return Assert(
        test=type_check(variable, types),
        msg=JoinedStr([Constant(f"type check failed: isinstance({variable}, {ast.unparse(types)}) evaluated to False."
                                " Actual type: "),
                       FormattedValue(
                            value=Attribute(Call(Name("type"), [Name(variable)], []), "__name__"),
                            conversion=-1)])
        #Constant()
        )


def guard(body: list[ast.stmt]):
    return If(test=Name('__debug__'),
                  body=body,
                  orelse=[])
