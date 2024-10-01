from _ast import AST, BinOp, Constant, List, Name, Subscript, Tuple, arguments
import ast
from ast import FunctionDef
from functools import cache
from pathlib import Path
from typing import Any, Optional, Type
from magic_typing.codegen import guard, assert_type


class Parser(ast.NodeVisitor):
    __slots__ = ['value']

    def __init__(self):
        self.value: Any = None

    def visit(self, node: Optional[ast.AST]):
        if node is None:
            return
        return super().visit(node)

def parse(parser_type: Type[Parser], node: Optional[ast.AST]):
    parser = parser_type()
    parser.visit(node)
    return parser.value

class TypeParser(Parser):
    def generic_visit(self, node: AST) -> Any:
        print(node)
        return super().generic_visit(node)

    def visit_Constant(self, node: Constant) -> Any:
        return node.value

    def visit_List(self, node: List) -> Any:
        return f"[{', '.join(self.visit(item) for item in node.elts)}]"

    def visit_Tuple(self, node: Tuple) -> Any:
        return [self.visit(item) for item in node.elts]


    def visit_Subscript(self, node: Subscript) -> Any:
        type_name = self.visit(node.value)
        args = self.visit(node.slice)

        return f"{type_name}[{', '.join([args] if isinstance(args, str) else args)}]"

    def visit_Name(self, node: Name) -> str:
        return node.id

    def visit_BinOp(self, node: BinOp):
        assert isinstance(node.op, ast.BitOr), "Unsupported operator in this context"
        return f"Union[{self.visit(node.left)}, {self.visit(node.right)}]"

class ArgumentList(Parser):
    def generic_visit(self, node: AST) -> Any:
        print(node)
        return super().generic_visit(node)

    def visit_Name(self, node: Name) -> Any:
        return node.id

    def visit_arguments(self, node: arguments) -> Any:
        for arg in node.args:
            yield self.visit(arg)
        # todo kwargs etc

    def visit_arg(self, node: ast.arg):
        name = node.arg
        annotation = TypeParser().visit(node.annotation) if node.annotation else None
        return name, annotation





class FunctionTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        # print(node.args)
        # args = parse(ArgumentList, node.args)
        # return_type = parse(TypeParser, node.returns)
        assertions: list[ast.stmt] = []
        for argument, annotation in ArgumentList().visit(node.args):
            if annotation is None:
                continue
            assertions.append(assert_type(argument, annotation))

        if assertions:
            node.body = [*assertions, *node.body]
        return super().generic_visit(node)

class Preprocessor(ast.NodeTransformer):
    def generic_visit(self, node: ast.AST):
        return super().generic_visit(node)

    def visit_FunctionDef(self, node: FunctionDef):
        return FunctionTransformer().visit(node)


class ModuleParser(ast.NodeVisitor):

    def visit_Name(self, node: ast.Name):
        print(node.id)
        return 7

def parse_module(module: ast.Module):
    assert isinstance(module, ast.Module)
    parser = ModuleParser()
    for statement in module.body:
        print(statement)
        parser.visit(statement)


@cache
def preprocess(data: str):
    tree = ast.parse(data[data.find('\n'):], type_comments=True)
    new_tree = Preprocessor().visit(tree)
    unparsed = ast.unparse(new_tree)
    # Comments are not preserved, prepend a newline.
    return '\n' + unparsed

if __name__ == "__main__":
    file = Path.cwd() / "test" / "test.py"
    # print(preprocess(file.read_text()))
    source = file.read_text()
    module = ModuleParser()
    # print(module.visit(ast.parse(source)))
    print(parse_module(ast.parse(source, type_comments=True)))
    print(ast.dump(ast.parse(source, type_comments=True), indent=4))#
 