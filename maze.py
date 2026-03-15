"""a_maze_ing module for maze generation."""

from typing import List, Dict, Tuple, Any
from random import seed, shuffle, randint

BLOCKED = -1
FOUR: List[tuple[int, int]] = [(0, 0), (0, 1), (0, 2), (1, 2),
                               (2, 2), (2, 3), (2, 4)]
TWO: List[tuple[int, int]] = [(0, 0), (1, 0), (2, 0), (2, 1),
                              (2, 2), (1, 2), (0, 2), (0, 3),
                              (0, 4), (1, 4), (2, 4)]


class MazeGenerator:
    """Generates a maze using the backtracker algorithm."""

    def __init__(self, width: int, height: int, pattern: bool = False) -> None:
        """Initialize the MazeGenerator with a given width and height.

        Args:
            width: The width of the maze in cells.
            height: The height of the maze in cells.
            pattern: Whether to place the 42 pattern. Defaults to False.

        Attributes:
            grid: 2D list of integers representing the maze cells.
                  0 = normal cell, -1 = blocked cell.
        """
        self.width: int = width
        self.height: int = height
        self.grid: List[List[int]] = []
        for y in range(height):
            row: List[int] = []
            for x in range(width):
                row.append(15)
            self.grid.append(row)
        if pattern:
            self.place_pattern()

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

    def generate_maze(self, config_dict: Dict[str, Any]) -> None:
        """Use backtracking to generate a maze in the grid.

        Args:
            config_dict: Dict containing parsed config values.
        """
        entry: Tuple[int, int] = config_dict["ENTRY"]
        if config_dict.get("SEED", None):
            seed(config_dict["SEED"])
        self._backtrack(*entry)
        if not config_dict["PERFECT"]:
            self._remove_walls()
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
        """Remove additional walls to generate a non-perfect maze."""
        to_remove = int(self.width * self.height * 0.1)
        while to_remove:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)
            dirs = [(0, -1, 1, 4), (0, 1, 4, 1), (-1, 0, 8, 2), (1, 0, 2, 8)]
            shuffle(dirs)
            if (self.grid[y][x] != -1
                    and self.grid[y + dirs[0][1]][x + dirs[0][0]] != -1):
                self.grid[y][x] &= ~dirs[0][2]
                self.grid[y + dirs[0][1]][x + dirs[0][0]] &= ~dirs[0][3]
                to_remove -= 1
