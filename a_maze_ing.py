#!/usr/bin/env python3

from sys import argv, exit
from typing import List, Dict
from maze import MazeGenerator


def parse_value(config_dict: Dict, key: str, conversion: str) -> None:
    try:
        if conversion == "str":
            config_dict[key]
        elif conversion == "int":
            config_dict[key] = int(config_dict[key])
        elif conversion == "tuple":
            temp: List = config_dict[key].split(",")
            if len(temp) != 2:
                raise ValueError("Tuple must have 2 values!")
            temp_int: List = [int(nbr) for nbr in temp]
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


def parse_config() -> Dict:
    try:
        file: str = argv[1]
    except IndexError:
        print(f"Usage: python3 {argv[0]} <config file>")
        exit()
    config_list: List = []
    try:
        with open(file) as f:
            for line in f:
                if not line.startswith("#") and line.strip():
                    config_list.append(line.strip())
    except FileNotFoundError:
        print(f"File {file} not found. Please make sure it exists!")
        exit()
    config_dict: Dict = {}
    try:
        for item in config_list:
            split_item: List = item.split("=")
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
    parse_value(config_dict, "SEED", "str")
    return config_dict


def validate_config(config_dict: Dict) -> bool:
    if config_dict["WIDTH"] < 1 or config_dict["HEIGHT"] < 1:
        return False
    if (config_dict["ENTRY"][0] >= config_dict["WIDTH"]
            or config_dict["ENTRY"][0] < 0
            or config_dict["ENTRY"][1] >= config_dict["HEIGHT"]
            or config_dict["ENTRY"][1] < 0):
        return False
    if (config_dict["EXIT"][0] >= config_dict["WIDTH"]
            or config_dict["EXIT"][0] < 0
            or config_dict["EXIT"][1] >= config_dict["HEIGHT"]
            or config_dict["EXIT"][1] < 0):
        return False
    if config_dict["ENTRY"] == config_dict["EXIT"]:
        return False
    if not config_dict["OUTPUT_FILE"]:
        return False
    return True


def test_output(maze: MazeGenerator, hex: bool) -> None:
    for row in maze.grid:
        for col in row:
            if hex:
                print(f"{col:x}", end="")
            elif (col == -1):
                print("#", end="")
            else:
                print("_", end="")
        print()


def create_output_file(maze: MazeGenerator, config_dict: Dict) -> None:
    output_string = ""
    for row in maze.grid:
        for col in row:
            output_string += f"{col:x}"
        output_string += "\n"
    output_string += f"\n{config_dict['ENTRY'][0]},{config_dict['ENTRY'][1]}\n"
    output_string += f"{config_dict['EXIT'][0]},{config_dict['EXIT'][1]}\n"
    output_string += "[SOLUTION PATH HERE]\n"
    try:
        with open(config_dict["OUTPUT_FILE"], "w") as f:
            f.write(output_string)
    except Exception as e:
        print(f"Error while creating {config_dict['OUTPUT_FILE']}: {e}")


def main() -> None:
    config_dict: Dict = parse_config()
    maze = MazeGenerator(config_dict["WIDTH"], config_dict["HEIGHT"], True)
    # test_output(maze, True)
    create_output_file(maze, config_dict)


if __name__ == "__main__":
    main()
