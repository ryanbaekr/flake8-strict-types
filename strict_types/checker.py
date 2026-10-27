"""Force a type annotation on every assignment"""

import libcst as cst
from libcst.metadata import PositionProvider
from typing import Any, Generator, List, Tuple, Type

OKAY: Tuple[Type[Any], Type[Any]] = (cst.Subscript, cst.Attribute)


class StrictTypeVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, errors: List[Tuple[int, int, str]]) -> None:
        self.errors: List[Tuple[int, int, str]] = errors

    def visit_Assign(self, node: cst.Assign) -> None:
        """Flag standard assignments like 'x = 1'"""
        pos = self.get_metadata(PositionProvider, node)

        if all(not isinstance(target.target, OKAY) for target in node.targets):
            self.errors.append((
                pos.start.line,
                pos.start.column,
                "TYP001 missing type annotation for variable",
            ))


class Plugin:
    name: str = "strict_types"
    version: str = "0.3.0"

    def __init__(self, lines: List[str]) -> None:
        self.source: str = "\n".join(lines)

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        errors: List[Tuple[int, int, str]] = []
        tree = cst.parse_module(self.source)
        wrapper = cst.MetadataWrapper(tree)
        visitor: StrictTypeVisitor = StrictTypeVisitor(errors)

        wrapper.visit(visitor)

        for lineno, colno, msg in errors:
            yield lineno, colno, msg, type(self)
