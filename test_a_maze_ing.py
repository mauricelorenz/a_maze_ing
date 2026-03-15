from os import remove
from pytest import raises
from a_maze_ing import parse_config, validate_config, parse_value


def test_parse_config_happy() -> None:
    conf_file = "test_parse_config_happy.txt"
    conf_content = """# Comment
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=12345678
"""
    with open(conf_file, "w") as f:
        f.write(conf_content)
    try:
        assert parse_config(conf_file) == {"WIDTH": 20,
                                           "HEIGHT": 15,
                                           "ENTRY": (0, 0),
                                           "EXIT": (19, 14),
                                           "OUTPUT_FILE": "maze.txt",
                                           "PERFECT": True,
                                           "SEED": "12345678"}
    finally:
        remove(conf_file)


def test_parse_config_seedless() -> None:
    conf_file = "test_parse_config_seedless.txt"
    conf_content = """# Comment
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    with open(conf_file, "w") as f:
        f.write(conf_content)
    try:
        assert parse_config(conf_file) == {"WIDTH": 20,
                                           "HEIGHT": 15,
                                           "ENTRY": (0, 0),
                                           "EXIT": (19, 14),
                                           "OUTPUT_FILE": "maze.txt",
                                           "PERFECT": True}
    finally:
        remove(conf_file)


def test_validate_config_happy() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (0, 0),
         "EXIT": (19, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert validate_config(d)


def test_validate_config_width_neg() -> None:
    d = {"WIDTH": -20,
         "HEIGHT": 15,
         "ENTRY": (0, 0),
         "EXIT": (19, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_height_neg() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": -15,
         "ENTRY": (0, 0),
         "EXIT": (19, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_entry_x_low() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (-100, 0),
         "EXIT": (19, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_entry_x_high() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (100, 0),
         "EXIT": (19, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_entry_y_low() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (0, -100),
         "EXIT": (19, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_entry_y_high() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (0, 100),
         "EXIT": (19, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_exit_x_low() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (0, 0),
         "EXIT": (-100, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_exit_x_high() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (0, 0),
         "EXIT": (100, 14),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_exit_y_low() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (0, 0),
         "EXIT": (19, -100),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_exit_y_high() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (0, 0),
         "EXIT": (19, 100),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_entry_eq_exit() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (10, 10),
         "EXIT": (10, 10),
         "OUTPUT_FILE": "maze.txt",
         "PERFECT": True}
    assert not validate_config(d)


def test_validate_config_empty_outfile() -> None:
    d = {"WIDTH": 20,
         "HEIGHT": 15,
         "ENTRY": (0, 0),
         "EXIT": (19, 14),
         "OUTPUT_FILE": "",
         "PERFECT": True}
    assert not validate_config(d)


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


def test_parse_value_bool_key_error() -> None:
    d = {"PERFECT": "True"}
    with raises(SystemExit):
        parse_value(d, "FOO", "bool")


def test_parse_value_bool_foo() -> None:
    d = {"PERFECT": "Foo"}
    with raises(SystemExit):
        parse_value(d, "PERFECT", "bool")
