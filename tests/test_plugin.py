"""Test the behavior of the plugin"""

import ast

from strict_types.checker import Plugin


def test_no_annotation() -> None:
    """Test that an error is produced"""

    code = "x = 1"
    tree = ast.parse(code)
    plugin = Plugin(tree)

    for _, _, msg, _ in plugin.run():
        assert msg == "TYP001 missing type annotation for variable"
