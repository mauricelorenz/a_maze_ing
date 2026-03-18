"""a_maze_ing module for parsing config file."""

from sys import exit
from typing import List, Dict, Any


def parse_value(config_dict: Dict[str, Any],
                key: str, conversion: str) -> None:
    """Turn the dict values from string into destination type.

    Args:
        config_dict: Dict containing parsed config values.
        key: Key for the value to be cast.
        conversion: Desired type for the value.
    """
    try:
        if conversion == "str":
            config_dict[key]
        elif conversion == "int":
            config_dict[key] = int(config_dict[key])
        elif conversion == "tuple":
            temp: List[str] = config_dict[key].split(",")
            if len(temp) != 2:
                raise ValueError("Tuple must have 2 values!")
            temp_int: List[int] = [int(nbr) for nbr in temp]
            config_dict[key] = tuple(temp_int)
        elif conversion == "bool":
            if config_dict[key] == "True":
                config_dict[key] = True
            elif config_dict[key] == "False":
                config_dict[key] = False
            else:
                raise Exception("Invalid string for bool!")
    except KeyError:
        print(f"Error while parsing {key}: missing argument")
        exit()
    except Exception as e:
        print(f"Error while parsing {key}: {e}")
        exit()


def parse_config(file: str) -> Dict[str, Any]:
    """Read and parse configuration file.

    Args:
        file: A file containing key value pairs.

    Returns:
        Dict containing parsed config values.
    """
    config_list: List[str] = []
    try:
        with open(file) as f:
            for line in f:
                if not line.startswith("#") and line.strip():
                    config_list.append(line.strip())
    except FileNotFoundError:
        print(f"File {file} not found. Please make sure it exists!")
        exit()
    config_dict: Dict[str, Any] = {}
    try:
        for item in config_list:
            split_item: List[str] = item.split("=")
            if len(split_item) != 2:
                raise Exception("Invalid key value pairs!")
            config_dict[split_item[0]] = split_item[1]
    except Exception as e:
        print(f"Error: {e}")
        exit()
    parse_value(config_dict, "WIDTH", "int")
    parse_value(config_dict, "HEIGHT", "int")
    parse_value(config_dict, "ENTRY", "tuple")
    parse_value(config_dict, "EXIT", "tuple")
    parse_value(config_dict, "OUTPUT_FILE", "str")
    parse_value(config_dict, "PERFECT", "bool")
    if "PATTERN" in config_dict:
        parse_value(config_dict, "PATTERN", "bool")
    if not validate_config(config_dict):
        exit()
    return config_dict


def validate_config(config_dict: Dict[str, Any]) -> bool:
    """Check config_dict for invalid values.

    Args:
        config_dict: Dict containing parsed config values.

    Returns:
        True if all parameters are valid, else False.
    """
    invalid_list: List[str] = []
    if config_dict["WIDTH"] < 1 or config_dict["HEIGHT"] < 1:
        invalid_list.append("WIDTH and HEIGHT must be positive!")
    if (config_dict["ENTRY"][0] >= config_dict["WIDTH"]
            or config_dict["ENTRY"][0] < 0
            or config_dict["ENTRY"][1] >= config_dict["HEIGHT"]
            or config_dict["ENTRY"][1] < 0):
        invalid_list.append("ENTRY must be within boundaries!")
    if (config_dict["EXIT"][0] >= config_dict["WIDTH"]
            or config_dict["EXIT"][0] < 0
            or config_dict["EXIT"][1] >= config_dict["HEIGHT"]
            or config_dict["EXIT"][1] < 0):
        invalid_list.append("EXIT must be within boundaries!")
    if config_dict["ENTRY"] == config_dict["EXIT"]:
        invalid_list.append("EXIT must not be at the same position as ENTRY!")
    if not config_dict["OUTPUT_FILE"]:
        invalid_list.append("OUTPUT_FILE must not be empty!")
    if invalid_list:
        if len(invalid_list) == 1:
            print(f"Input validation failed: {invalid_list[0]}")
            return False
        print("Input validation failed:")
        for item in invalid_list:
            print(f"  {item}")
        return False
    return True
