"""a_maze_ing module for file output."""

from mazegen import MazeGenerator


def create_output_file(maze: MazeGenerator) -> None:
    """Create the predefined output file from the created maze.

    Args:
        maze: Maze instance containing grid, entry, exit, and path.
    """
    output_string: str = ""
    for row in maze.grid:
        for col in row:
            output_string += f"{col:X}"
        output_string += "\n"
    output_string += f"\n{maze.entry[0]},{maze.entry[1]}\n"
    output_string += f"{maze.exit[0]},{maze.exit[1]}\n"
    output_string += f"{''.join(maze.path)}\n"
    try:
        with open(maze.output_file, "w") as f:
            f.write(output_string)
    except Exception as e:
        print(f"Error while creating {maze.output_file}: {e}")
