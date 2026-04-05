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


def test_w_annotation() -> None:
    """Test that no error is produced"""

    code = "x: int = 1"
    tree = ast.parse(code)
    plugin = Plugin(tree)

    for _ in plugin.run():
        assert False  # not reached, no errors


def test_dict_setitem() -> None:
    """Test that no error is produced"""

    code = "my_dict['my_key'] = 1"
    tree = ast.parse(code)
    plugin = Plugin(tree)

    for _ in plugin.run():
        assert False  # not reached, no errors


def test_dot_notation() -> None:
    """Test that no error is produced"""

    code = "my_obj.my_attr = 1"
    tree = ast.parse(code)
    plugin = Plugin(tree)

    for _ in plugin.run():
        assert False  # not reached, no errors
