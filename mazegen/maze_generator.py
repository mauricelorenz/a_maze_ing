"""a_maze_ing module for maze generation."""

from typing import List, Dict, Any, Deque, Tuple, Set
from random import seed, shuffle, randint
from collections import deque

BLOCKED = -1
FOUR: List[tuple[int, int]] = [(0, 0), (0, 1), (0, 2), (1, 2),
                               (2, 2), (2, 3), (2, 4)]
TWO: List[tuple[int, int]] = [(0, 0), (1, 0), (2, 0), (2, 1),
                              (2, 2), (1, 2), (0, 2), (0, 3),
                              (0, 4), (1, 4), (2, 4)]


class MazeGenerator:
    """Generates a maze using the backtracker algorithm."""

    def __init__(self, config_dict: Dict[str, Any]) -> None:
        """Initialize the MazeGenerator with a given width and height.

        Args:
            config_dict: Dict containing parsed config values.
                         Required keys: WIDTH, HEIGHT.
                         Optional keys: PATTERN (bool, defaults to False).

        Attributes:
            grid: 2D list of integers representing the maze cells.
                  15 = all walls closed, -1 = blocked cell (42 pattern).
            config: Dict containing parsed config values.
        """
        self.width = config_dict["WIDTH"]
        self.height = config_dict["HEIGHT"]
        self.config = config_dict
        self.grid: List[List[int]] = []
        self.path: List[str] = []
        for y in range(self.height):
            row: List[int] = []
            for x in range(self.width):
                row.append(15)
            self.grid.append(row)
        if (config_dict.get("PATTERN", False)):
            self.place_pattern()

    def place_pattern(self) -> None:
        """Place the 42 pattern and set these cells as BLOCKED (-1).

        Prints an error and returns early if the maze is too small
        (minimum 11x9 required.)
        """
        if self.width < 11 or self.height < 9:
            print("\nMaze too small to place 42 pattern!")
            return
        start_x: int = (self.width // 2) - 3
        start_y: int = (self.height // 2) - 2
        for (px, py) in FOUR:
            if ((start_x + px, start_y + py) == self.config["ENTRY"]
                    or (start_x + px, start_y + py) == self.config["EXIT"]):
                print("ENTRY and EXIT must not be in 42 pattern!")
                exit(1)
            self.grid[start_y + py][start_x + px] = BLOCKED
        for (px, py) in TWO:
            if ((start_x + px, start_y + py) == self.config["ENTRY"]
                    or (start_x + px, start_y + py) == self.config["EXIT"]):
                print("ENTRY and EXIT must not be in 42 pattern!")
                exit(1)
            self.grid[start_y + py][start_x + px + 4] = BLOCKED

    def generate_maze(self) -> None:
        """Use backtracking to generate a maze in the grid.

        Args:
            config_dict: Dict containing parsed config values.
        """
        entry = self.config["ENTRY"]
        if self.config.get("SEED", None):
            seed(self.config["SEED"])
        else:
            seed()
        try:
            self._backtrack(*entry)
        except RecursionError as e:
            print(f"Error: {e}")
            exit(1)
        if not self.config["PERFECT"]:
            self._remove_walls()
            self._force_second_path()
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                if col == -1:
                    self.grid[r][c] = 15

    def _backtrack(self, x: int, y: int) -> None:
        """Recursively call the backtracking algorithm to remove walls.

        Args:
            x: x value of the current position.
            y: y value of the current position.
        """
        dirs = [(0, -1, 1, 4), (0, 1, 4, 1), (-1, 0, 8, 2), (1, 0, 2, 8)]
        shuffle(dirs)
        for dir in dirs:
            if (self._is_in_bounds(x + dir[0], y + dir[1])
                    and self.grid[y + dir[1]][x + dir[0]] == 15):
                self.grid[y][x] &= ~dir[2]
                self.grid[y + dir[1]][x + dir[0]] &= ~dir[3]
                self._backtrack(x + dir[0], y + dir[1])

    def _is_in_bounds(self, x: int, y: int) -> bool:
        """Check if current position is in the grid's boundaries.

        Args:
            x: x value of the current position.
            y: y value of the current position.

        Returns:
            True if position is in boundaries, else False.
        """
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return False
        return True

    def _remove_walls(self) -> None:
        """Remove approximately 10% of walls randomly to create loops.

        Skips walls that would create a 3x3 open area. Stopfs after a maximum
        number of tries to prevent an infinte loop.
        """
        to_remove = int(self.width * self.height * 0.1)
        max_tries = int(self.width * self.height * 10)
        tries: int = 0
        while to_remove and tries < max_tries:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)
            dirs = [(0, -1, 1, 4), (0, 1, 4, 1), (-1, 0, 8, 2), (1, 0, 2, 8)]
            shuffle(dirs)
            if (self.grid[y][x] != -1
                    and self.grid[y + dirs[0][1]][x + dirs[0][0]] != -1
                    and not self._would_create_3x3(x, y)):
                self.grid[y][x] &= ~dirs[0][2]
                self.grid[y + dirs[0][1]][x + dirs[0][0]] &= ~dirs[0][3]
                to_remove -= 1
            tries += 1

    def _would_create_3x3(self, x: int, y: int) -> bool:
        """Check if removing a wall would create a 3x3 open area around (x, y).

        Args:
            x: x value of the center position.
            y: y value of the center position.

        Returns:
            True if a 3x3 open area exists, else False.
        """
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx = x + dx
                ny = y + dy
                if self._is_in_bounds(nx + 1, ny):
                    if self.grid[ny][nx] & 2 != 0:
                        return False
                if self._is_in_bounds(nx, ny + 1):
                    if self.grid[ny][nx] & 4 != 0:
                        return False
        return True

    def solve(self) -> List[str]:
        """Solve the maze using BFS and return the shortest path.

        Returns:
            List of directions as strings (N, E, S, W).
        """
        entry = self.config["ENTRY"]
        exit_ = self.config["EXIT"]
        queue: Deque[Tuple[int, int]] = deque()
        queue.append(entry)
        visited: Set[Tuple[int, int]] = {entry}
        came_from: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}
        while queue:
            current = queue.popleft()
            if current == exit_:
                break
            dirs = [(0, -1, 1, "N"), (0, 1, 4, "S"),
                    (-1, 0, 8, "W"), (1, 0, 2, "E")]
            for dir in dirs:
                nx = current[0] + dir[0]
                ny = current[1] + dir[1]
                neighbor = (nx, ny)
                if (self._is_in_bounds(nx, ny)
                        and neighbor not in visited
                        and self.grid[current[1]][current[0]] & dir[2] == 0):
                    queue.append(neighbor)
                    visited.add(neighbor)
                    came_from[neighbor] = (current, dir[3])
        current = exit_
        self.path = []
        while current != entry:
            previous, direction = came_from[current]
            self.path.append(direction)
            current = previous
        self.path.reverse()
        return self.path

    def _force_second_path(self) -> None:
        """Force a second path by opening an additional wall at entry."""
        x, y = self.config["ENTRY"]
        dirs = [(0, -1, 1, 4), (0, 1, 4, 1), (-1, 0, 8, 2), (1, 0, 2, 8)]
        shuffle(dirs)
        for d in dirs:
            nx = x + d[0]
            ny = y + d[1]
            if (self._is_in_bounds(nx, ny)
                    and self.grid[ny][nx] != -1
                    and self.grid[y][x] & d[2] != 0
                    and not self._would_create_3x3(x, y)):
                self.grid[y][x] &= ~d[2]
                self.grid[ny][nx] &= ~d[3]
                return
