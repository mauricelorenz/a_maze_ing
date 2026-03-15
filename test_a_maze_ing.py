from pytest import raises
from a_maze_ing import parse_value


def test_parse_value_str_happy() -> None:
    d = {"OUTPUT_FILE": "maze.txt"}
    parse_value(d, "OUTPUT_FILE", "str")
    assert d["OUTPUT_FILE"] == "maze.txt"


def test_parse_value_str_key_error() -> None:
    d = {"OUTPUT_FILE": "maze.txt"}
    with raises(SystemExit):
        parse_value(d, "FOO", "str")


def test_parse_value_int_happy() -> None:
    d = {"WIDTH": "1"}
    parse_value(d, "WIDTH", "int")
    assert d["WIDTH"] == 1


def test_parse_value_int_key_error() -> None:
    d = {"WIDTH": "1"}
    with raises(SystemExit):
        parse_value(d, "FOO", "int")


def test_parse_value_int_value_error() -> None:
    d = {"WIDTH": "abc"}
    with raises(SystemExit):
        parse_value(d, "WIDTH", "int")


def test_parse_value_tuple_happy() -> None:
    d = {"ENTRY": "0,0"}
    parse_value(d, "ENTRY", "tuple")
    assert d["ENTRY"] == (0, 0)


def test_parse_value_tuple_key_error() -> None:
    d = {"ENTRY": "0,0"}
    with raises(SystemExit):
        parse_value(d, "FOO", "tuple")


def test_parse_value_tuple_alpha() -> None:
    d = {"ENTRY": "1,abc"}
    with raises(SystemExit):
        parse_value(d, "ENTRY", "tuple")


def test_parse_value_tuple_too_few() -> None:
    d = {"ENTRY": "1"}
    with raises(SystemExit):
        parse_value(d, "ENTRY", "tuple")


def test_parse_value_tuple_too_many() -> None:
    d = {"ENTRY": "1,2,3"}
    with raises(SystemExit):
        parse_value(d, "ENTRY", "tuple")


def test_parse_value_bool_true() -> None:
    d = {"PERFECT": "True"}
    parse_value(d, "PERFECT", "bool")
    assert d["PERFECT"] is True


def test_parse_value_bool_false() -> None:
    d = {"PERFECT": "False"}
    parse_value(d, "PERFECT", "bool")
    assert d["PERFECT"] is False


def test_parse_value_bool_foo() -> None:
    d = {"PERFECT": "Foo"}
    with raises(SystemExit):
        parse_value(d, "PERFECT", "bool")
