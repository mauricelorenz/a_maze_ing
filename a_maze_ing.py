"""a_maze_ing main program to be run directly."""

from sys import argv, exit
from typing import Dict, Any, List
from config_parser import parse_config
from file_output import create_output_file
from mazegen import MazeGenerator
from maze_renderer import render_maze
from bonus_image_renderer import render_image


def main_loop(file: str) -> None:
    """Loop through maze output and user input.

    Args:
        file: Name of the config file.
    """
    choice: str = "1"
    show_path: bool = False
    wall_colors: List[str] = ["\033[37m", "\033[36m", "\033[35m"]
    while True:
        if choice == "0":
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Bonus: Show and save maze as PNG")
            print("5. Quit")
            choice = input("Choice? (1-5): ")
        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice. Try again!")
        elif choice == "1":
            config_dict: Dict[str, Any] = parse_config(file)
            maze: MazeGenerator = MazeGenerator(config_dict)
            maze.generate_maze()
            maze.solve()
            create_output_file(maze)
            print()
            rendered_maze: List[List[int]] = render_maze(maze,
                                                         show_path,
                                                         wall_colors[0])
        elif choice == "2":
            show_path = not show_path
            print()
            rendered_maze = render_maze(maze, show_path, wall_colors[0])
        elif choice == "3":
            wall_colors.append(wall_colors.pop(0))
            print()
            render_maze(maze, show_path, wall_colors[0])
        elif choice == "4":
            render_image(maze, rendered_maze)
        elif choice == "5":
            break
        choice = "0"


def main() -> None:
    """Run the main program."""
    try:
        file: str = argv[1]
    except IndexError:
        print(f"Usage: python3 {argv[0]} <config file>")
        exit(1)
    main_loop(file)


if __name__ == "__main__":
    main()
