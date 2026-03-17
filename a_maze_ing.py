#!/usr/bin/env python3

"""a_maze_ing main program to be run directly."""

from sys import argv, exit
from typing import List, Dict, Any
from maze import MazeGenerator
from render_maze import render_maze


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


# Only for development. Remove before turning in
def test_output(maze: MazeGenerator, hex: bool) -> None:
    """Output test function."""
    for row in maze.grid:
        for col in row:
            if hex:
                print(f"{col:X}", end="")
            elif (col == -1):
                print("#", end="")
            else:
                print("_", end="")
        print()


def create_output_file(maze: MazeGenerator) -> None:
    """Create the predefined output file from the created maze.

    Args:
        maze: Maze instance containing grid, entry, exit, and solution.
        config_dict: Dict containing parsed config values.
        path: List of directions as strings(N, E, S, W).
    """
    output_string = ""
    for row in maze.grid:
        for col in row:
            output_string += f"{col:X}"
        output_string += "\n"
    output_string += f"\n{maze.config['ENTRY'][0]},{maze.config['ENTRY'][1]}\n"
    output_string += f"{maze.config['EXIT'][0]},{maze.config['EXIT'][1]}\n"
    output_string += "".join(maze.path) + "\n"
    try:
        with open(maze.config["OUTPUT_FILE"], "w") as f:
            f.write(output_string)
    except Exception as e:
        print(f"Error while creating {maze.config['OUTPUT_FILE']}: {e}")


def main_loop(maze: MazeGenerator, file: str) -> None:
    choice = "0"
    show_path = False
    wall_colors = ["\033[37m", "\033[36m", "\033[35m"]
    while choice != "4":
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = input("Choice? (1-4): ")
        print()
        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Try again!")
            choice = "0"
        elif choice == "1":
            config_dict: Dict[str, Any] = parse_config(file)
            maze = MazeGenerator(config_dict)
            maze.generate_maze()
            maze.solve()
            create_output_file(maze)
            render_maze(maze, show_path, wall_colors[0])
        elif choice == "2":
            show_path = not show_path
            render_maze(maze, show_path, wall_colors[0])
        elif choice == "3":
            wall_colors.append(wall_colors.pop(0))
            render_maze(maze, show_path, wall_colors[0])


def main() -> None:
    """Run the main program."""
    try:
        file: str = argv[1]
    except IndexError:
        print(f"Usage: python3 {argv[0]} <config file>")
        exit()
    config_dict: Dict[str, Any] = parse_config(file)
    maze = MazeGenerator(config_dict)
    maze.generate_maze()
    maze.solve()
    create_output_file(maze)
    render_maze(maze, False)
    main_loop(maze, file)


if __name__ == "__main__":
    main()
