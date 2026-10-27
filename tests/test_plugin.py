"""Test the behavior of the plugin"""

from strict_types.checker import Plugin


def test_no_annotation() -> None:
    """Test that an error is produced"""

    code = "x = 1"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) > 0

    for _, _, msg, _ in plugin.run():
        assert msg == "TYP001 missing type annotation for variable"


def test_w_annotation() -> None:
    """Test that no error is produced"""

    code = "x: int = 1"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_dict_setitem() -> None:
    """Test that no error is produced"""

    code = "my_dict['my_key'] = 1"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_dot_notation() -> None:
    """Test that no error is produced"""

    code = "my_obj.my_attr = 1"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_reassignment() -> None:
    """Test that no error is produced"""

    code = "my_int: int = 6\nmy_int = 7"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_global() -> None:
    """Test that no error is produced"""

    code = "my_int: int = 6\n\ndef foo():\n    global my_int\n    my_int = 7"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_global_shadow() -> None:
    """Test that an error is produced"""

    code = "my_int: int = 6\n\ndef foo():\n    my_int = 7"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) > 0

    for _, _, msg, _ in plugin.run():
        assert msg == "TYP001 missing type annotation for variable"


def test_nonlocal() -> None:
    """Test that no error is produced"""

    code = (
        "def outer():\n    my_int: int = 6\n    def inner():"
        "\n        nonlocal my_int\n        my_int = 7"
    )
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_nonlocal_shadow() -> None:
    """Test that an error is produced"""

    code = (
        "def outer():\n    my_int: int = 6\n    def inner():"
        "\n        my_int = 7"
    )
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) > 0

    for _, _, msg, _ in plugin.run():
        assert msg == "TYP001 missing type annotation for variable"


def test_nested_global() -> None:
    """Test that no error is produced"""

    code = (
        "my_int: int = 6\n\ndef outer():\n    def inner():"
        "\n        global my_int\n        my_int = 7"
    )
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_global_no_definition() -> None:
    """Test that an error is produced"""

    code = "def foo():\n    global my_int\n    my_int = 7"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) > 0

    for _, _, msg, _ in plugin.run():
        assert msg == "TYP001 missing type annotation for variable"


def test_class_attribute() -> None:
    """Test that an error is produced"""

    code = "my_int: int = 6\n\nclass Foo:\n    my_int = 7"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) > 0

    for _, _, msg, _ in plugin.run():
        assert msg == "TYP001 missing type annotation for variable"


def test_class_reassignment() -> None:
    """Test that no error is produced"""

    code = "class Foo:\n    my_int: int = 6\n    my_int = 7"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_bare_annotation() -> None:
    """Test that no error is produced"""

    code = "my_int: int\n\ndef foo():\n    global my_int\n    my_int = 7"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) == 0


def test_sibling_scopes() -> None:
    """Test that an error is produced for each scope"""

    code = "def foo():\n    x: int = 1\ndef bar():\n    x = 2"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) > 0

    for _, _, msg, _ in run_output:
        assert msg == "TYP001 missing type annotation for variable"


def test_builtin_shadow() -> None:
    """Test that an error is produced"""

    code = "len = 5"
    lines = code.splitlines()
    plugin = Plugin(None, None, lines)

    run_output = [output for output in plugin.run()]
    assert len(run_output) > 0

    for _, _, msg, _ in plugin.run():
        assert msg == "TYP001 missing type annotation for variable"
