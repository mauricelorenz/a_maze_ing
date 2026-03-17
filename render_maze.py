from maze import MazeGenerator
from typing import List, Tuple, Dict


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


def set_special_cell(cell_value: int, coords: Tuple[int, int],
                     rendered_maze: List[List[int]]) -> None:
    for y in range(1, 3):
        for x in range(1, 3):
            rendered_maze[coords[1] * 3 + y][coords[0] * 3 + x] = cell_value


def render_special_cells(maze: MazeGenerator,
                         rendered_maze: List[List[int]]) -> None:
    set_special_cell(2, maze.config["ENTRY"], rendered_maze)
    set_special_cell(3, maze.config["EXIT"], rendered_maze)
    for r, row in enumerate(maze.grid):
        for c, col in enumerate(row):
            if maze.grid[r][c] == 15:
                set_special_cell(4, (c, r), rendered_maze)


def render_path(maze: MazeGenerator, rendered_maze: List[List[int]]) -> None:
    curr: Tuple[int, int] = maze.config["ENTRY"]
    path: List[str] = maze.path
    path_mapping: Dict[str, Tuple[int, int]] = {"N": (-1, 0),
                                                "E": (0, 1),
                                                "S": (1, 0),
                                                "W": (0, -1)}
    for s, step in enumerate(path):
        if s == len(path) - 1:
            break
        curr = (curr[0] + path_mapping[step][1],
                curr[1] + path_mapping[step][0])
        set_special_cell(5, curr, rendered_maze)


def print_maze(rendered_maze: List[List[int]], wall_color: str) -> None:
    entry = "\033[32m"
    exit_ = "\033[31m"
    pattern = "\033[34m"
    path = "\033[33m"
    reset = "\033[0m"
    for row in rendered_maze:
        for col in row:
            if (col == 1):
                print(wall_color + "█" + reset, end="")
            elif (col == 2):
                print(entry + "█" + reset, end="")
            elif (col == 3):
                print(exit_ + "█" + reset, end="")
            elif (col == 4):
                print(pattern + "█" + reset, end="")
            elif (col == 5):
                print(path + "█" + reset, end="")
            else:
                print(" ", end="")
        print()


def render_maze(maze: MazeGenerator, show_path: bool,
                wall_color: str = "\033[37m") -> None:
    rendered_maze = render_maze_grid(maze)
    render_special_cells(maze, rendered_maze)
    if show_path:
        render_path(maze, rendered_maze)
    print_maze(rendered_maze, wall_color)
