import ast
from magic_typing.preprocessor import TypeParser

def parse_type(code: str):
    tree = ast.parse(f"foo: ({code})")
    assert len(tree.body) == 1
    for statement in tree.body:
        assert isinstance(statement, ast.AnnAssign)
        return TypeParser().visit(statement.annotation)

def test_type_simple():
    assert parse_type("int") == "int"
    assert parse_type("Foo") == "Foo"

def test_type_union():
    assert parse_type("int | str") == ("Union[int, str]")
    assert parse_type("int | str | Foo") == ("int", "str", "Foo")
    assert parse_type("(int | str) | Foo") == ("int", "str", "Foo")
    assert parse_type("int | (str | Foo)") == ("int", "str", "Foo")

def test_type_generic():
    assert parse_type("list[int]") == ("list[int]")
    print(parse_type("dict[int, str]"))
    # assert parse_type("dict[int, str]") == ("dict[int, str]")
    # assert parse_type("Callable[[int], None]") == "Callable[[int], None]"
    print(parse_type("list[int | str]"))

if __name__ == "__main__":
    test_type_simple()
    test_type_union()
    test_type_generic()