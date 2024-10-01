import ast
from magic_typing.preprocessor import ArgumentList

def parse_arglist(code: str):
    tree = ast.parse(f"def foo({code}): ...")
    for statement in tree.body:
        assert isinstance(statement, ast.FunctionDef)
        return list(ArgumentList().visit(statement.args))

def test_args():
    args = parse_arglist("test, bar: int")
    print(args)
    assert args == [('test', None), ('bar', 'int')]

    args = parse_arglist("bar: int | str | bool")
    print(args)
    assert args == [('bar', ('int', 'str', 'bool'))]

    args = parse_arglist("bar: list[int]")
    print(args)
    assert args == [('bar', ('int', 'str', 'bool'))]

if __name__ == "__main__":
    test_args()
