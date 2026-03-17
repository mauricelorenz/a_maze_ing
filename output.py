"""Output file module for a_maze_ing."""

from mazegen import MazeGenerator


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
