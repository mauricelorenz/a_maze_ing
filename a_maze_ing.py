#!/usr/bin/env python3

from sys import argv, exit
from typing import List, Dict


def parse_value(config_dict: Dict, key: str, conversion: str) -> None:
    try:
        if conversion == "str":
            config_dict[key]
        elif conversion == "int":
            config_dict[key] = int(config_dict[key])
        elif conversion == "tuple":
            temp: List = config_dict[key].split(",")
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


BLOCKED = -1
FOUR: List[tuple] = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4)]
TWO: List[tuple] = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2),
                    (0, 3), (0, 4), (1, 4), (2, 4)]


class MazeGenerator:
    """Geneates a maze using the backtracker algorithm."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize the MazeGenerator with a given width and height.
            grid: 2D list of integers representing the maze cells.
                  0 = normal cell, -1 = blocked cell.
        """

        self.width: int = width
        self.height: int = height
        self.grid: List[List[int]] = []
        for y in range(height):
            row: List[int] = []
            for x in range(width):
                row.append(0)
            self.grid.append(row)

    def place_pattern(self) -> None:
        """Place the 42 pattern and set these cells as BLOCKED (-1)."""

        if self.width < 11 or self.height < 9:
            print("Maze too small to place 42 pattern!")
            return
        
        start_x: int = (self.width // 2) - 3
        start_y: int = (self.height // 2) - 2
        for (px, py) in FOUR:
            self.grid[start_y + py][start_x + px] = BLOCKED
        for (px, py) in TWO:
            self.grid[start_y + py][start_x + px + 4] = BLOCKED


def main() -> None:
    config_dict: Dict = parse_config()
    maze = MazeGenerator(config_dict["WIDTH"], config_dict["HEIGHT"])


if __name__ == "__main__":
    main()
