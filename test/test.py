# coding: magic_typing

from magic_typing.test import bar
def foo(x: int):
    return bar(x) 

CONST: int = 3 # type: ignore

y = [1, 2] # type: list[int]

foo(3)

if __name__ == "__main__":
    foo("bar")