from maze import MazeGenerator
from typing import List, Tuple


def render_maze_grid(maze: MazeGenerator) -> List[List[int]]:
    rendered_grid: List[List[int]] = []
    rendered_width: int = maze.width * 3 + 1
    rendered_height: int = maze.height * 3 + 1
    for _ in range(rendered_height):
        rendered_grid.append([])
    for r, row in enumerate(maze.grid):
        for c, col in enumerate(row):
            if (maze.grid[r][c] & 1 or maze.grid[r][c] & 8
                or (r > 0 and c > 0
                    and (maze.grid[r - 1][c - 1] & 2
                         or maze.grid[r - 1][c - 1] & 4))):
                rendered_grid[r * 3].extend([1])
            else:
                rendered_grid[r * 3].extend([0])
            if maze.grid[r][c] & 1:
                rendered_grid[r * 3].extend([1, 1])
            else:
                rendered_grid[r * 3].extend([0, 0])
            if maze.grid[r][c] & 8:
                rendered_grid[r * 3 + 1].extend([1, 0, 0])
            else:
                rendered_grid[r * 3 + 1].extend([0, 0, 0])
            if maze.grid[r][c] & 8:
                rendered_grid[r * 3 + 2].extend([1, 0, 0])
            else:
                rendered_grid[r * 3 + 2].extend([0, 0, 0])
        for n in range(3):
            rendered_grid[r * 3 + n].append(1)
    for n in range(rendered_width):
        rendered_grid[rendered_height - 1].append(1)
    return rendered_grid


def render_entry_exit(maze: MazeGenerator,
                      rendered_maze: List[List[int]]) -> None:
    entry: Tuple[int, int] = maze.config["ENTRY"]
    exit_: Tuple[int, int] = maze.config["EXIT"]
    for y in range(1, 3):
        for x in range(1, 3):
            rendered_maze[entry[1] * 3 + y][entry[0] * 3 + x] = 2
            rendered_maze[exit_[1] * 3 + y][exit_[0] * 3 + x] = 3


def print_maze(rendered_maze: List[List[int]]) -> None:
    # wall = "\033[37m"
    entry = "\033[32m"
    exit_ = "\033[31m"
    reset = "\033[0m"
    for row in rendered_maze:
        for col in row:
            if (col == 1):
                print("█", end="")
            elif (col == 2):
                print(entry + "█" + reset, end="")
            elif (col == 3):
                print(exit_ + "█" + reset, end="")
            else:
                print(" ", end="")
        print()


def render_maze(maze: MazeGenerator) -> None:
    rendered_maze = render_maze_grid(maze)
    render_entry_exit(maze, rendered_maze)
    print_maze(rendered_maze)
