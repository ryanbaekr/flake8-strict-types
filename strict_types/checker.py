"""Force a type annotation on every assignment"""

import libcst as cst
from libcst.metadata import PositionProvider, ScopeProvider
from typing import Any, Generator, List, Tuple, Type


class StrictTypeVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider, ScopeProvider)

    def __init__(self, errors: List[Tuple[int, int, str]]) -> None:
        self.errors: List[Tuple[int, int, str]] = errors

    def visit_Assign(self, node: cst.Assign) -> None:
        """Flag standard assignments like 'x = 1'"""
        pos = self.get_metadata(PositionProvider, node)

        if len(node.targets) != 1:
            self.errors.append((
                pos.start.line,
                pos.start.column,
                "TYP002 use of unpacking",
            ))
            return

        scope = self.get_metadata(ScopeProvider, node)
        target = node.targets[0].target
        is_instantiation = False

        if isinstance(target, cst.Name):
            name = target.value

            # all assignments to this name, resolved through global
            # and nonlocal declarations as well as enclosing scopes
            if scope is not None:
                assignments = scope[name]
            else:
                assignments = set()

            # definitions in the current scope before the current assignment
            definitions = [
                a for a in assignments
                if hasattr(a, "node") and
                self.get_metadata(PositionProvider, a.node).start.line
                < pos.start.line
            ]

            if not definitions:
                is_instantiation = True

        if is_instantiation:
            self.errors.append((
                pos.start.line,
                pos.start.column,
                "TYP001 missing type annotation for variable",
            ))


class Plugin:
    name: str = "strict_types"
    version: str = "0.3.1"

    def __init__(self, tree: Any, filename: Any, lines: List[str]) -> None:
        self.source: str = "\n".join(lines)

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        errors: List[Tuple[int, int, str]] = []
        tree = cst.parse_module(self.source)
        wrapper = cst.MetadataWrapper(tree)
        visitor: StrictTypeVisitor = StrictTypeVisitor(errors)

        wrapper.visit(visitor)

        for lineno, colno, msg in errors:
            yield lineno, colno, msg, type(self)
