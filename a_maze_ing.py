#!/usr/bin/env python3

"""a_maze_ing main program to be run directly."""

from sys import argv, exit
from typing import Dict, Any
from config_parser import parse_config
from output import create_output_file
from maze_generator import MazeGenerator
from render_maze import render_maze

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
