"""Test the behavior of the plugin"""

from strict_types.checker import Plugin


def test_no_annotation() -> None:
    """Test that an error is produced"""

    code = "x = 1"
    lines = code.splitlines()
    plugin = Plugin(lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) > 0

    for _, _, msg, _ in plugin.run():
        assert msg == "TYP001 missing type annotation for variable"


def test_w_annotation() -> None:
    """Test that no error is produced"""

    code = "x: int = 1"
    lines = code.splitlines()
    plugin = Plugin(lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_dict_setitem() -> None:
    """Test that no error is produced"""

    code = "my_dict['my_key'] = 1"
    lines = code.splitlines()
    plugin = Plugin(lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_dot_notation() -> None:
    """Test that no error is produced"""

    code = "my_obj.my_attr = 1"
    lines = code.splitlines()
    plugin = Plugin(lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0
