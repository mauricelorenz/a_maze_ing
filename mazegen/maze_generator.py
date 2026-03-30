"""a_maze_ing module for maze generation."""

from typing import List, Dict, Deque, Tuple, Set
from random import seed, shuffle, randint
from collections import deque


class MazeGenerator:
    """Generates a maze using the backtracker algorithm."""

    DIRS: List[Tuple[int, int, int, int, str]] = [(0, -1, 1, 4, "N"),
                                                  (0, 1, 4, 1, "S"),
                                                  (-1, 0, 8, 2, "W"),
                                                  (1, 0, 2, 8, "E")]

    def __init__(self, width: int, height: int, entry: Tuple[int, int],
                 exit: Tuple[int, int], output_file: str, perfect: bool,
                 seed: str | None = None, pattern: bool = True) -> None:
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
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed_ = seed
        self.pattern = pattern
        self.grid: List[List[int]] = []
        self.path: List[str] = []
        for y in range(self.height):
            row: List[int] = []
            for x in range(self.width):
                row.append(15)
            self.grid.append(row)
        if self.pattern:
            self.place_pattern()

    def place_pattern(self) -> None:
        """Place the 42 pattern and set these cells as blocked (-1).

        Prints an error and returns early if the maze is too small
        (minimum 11x9 required.)
        """
        FOURTY_TWO: List[tuple[int, int]] = [(0, 0), (0, 1), (0, 2), (1, 2),
                                             (2, 2), (2, 3), (2, 4), (4, 0),
                                             (5, 0), (6, 0), (6, 1), (6, 2),
                                             (5, 2), (4, 2), (4, 3), (4, 4),
                                             (5, 4), (6, 4)]
        if self.width < 11 or self.height < 9:
            print("\nMaze too small to place 42 pattern!")
            return
        start_x: int = (self.width // 2) - 3
        start_y: int = (self.height // 2) - 2
        for (px, py) in FOURTY_TWO:
            if ((start_x + px, start_y + py) == self.entry
                    or (start_x + px, start_y + py) == self.exit):
                print("ENTRY and EXIT must not be in 42 pattern!")
                exit(1)
            self.grid[start_y + py][start_x + px] = -1

    def generate_maze(self) -> None:
        """Use backtracking to generate a maze in the grid.

        Args:
            config_dict: Dict containing parsed config values.
        """
        if self.seed_:
            seed(self.seed_)
        else:
            seed()
        try:
            self._backtrack(*self.entry)
        except RecursionError as e:
            print(f"Error: {e}")
            exit(1)
        if not self.perfect:
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
        dirs: List[Tuple[int, int, int, int, str]] = self.DIRS[:]
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
        to_remove: int = int(self.width * self.height * 0.1)
        max_tries: int = int(self.width * self.height * 10)
        dirs: List[Tuple[int, int, int, int, str]] = self.DIRS[:]
        while to_remove and max_tries:
            x: int = randint(1, self.width - 2)
            y: int = randint(1, self.height - 2)
            shuffle(dirs)
            if (self.grid[y][x] != -1
                    and (self.grid[y + dirs[0][1]][x + dirs[0][0]]
                         != -1)
                    and not self._would_create_3x3(x, y)):
                self.grid[y][x] &= ~dirs[0][2]
                self.grid[y + dirs[0][1]][x + dirs[0][0]] \
                    &= ~dirs[0][3]
                to_remove -= 1
            max_tries -= 1

    def _force_second_path(self) -> None:
        """Force a second path by opening an additional wall at entry."""
        x, y = self.entry
        dirs: List[Tuple[int, int, int, int, str]] = self.DIRS[:]
        shuffle(dirs)
        for dir in dirs:
            if (self._is_in_bounds(x + dir[0], y + dir[1])
                    and self.grid[y + dir[1]][x + dir[0]] != -1
                    and self.grid[y][x] & dir[2] != 0
                    and not self._would_create_3x3(x, y)):
                self.grid[y][x] &= ~dir[2]
                self.grid[y + dir[1]][x + dir[0]] &= ~dir[3]
                return

    def _would_create_3x3(self, x: int, y: int) -> bool:
        """Check if removing a wall would create a 3x3 open area around (x, y).

        Args:
            x: x value of the center position.
            y: y value of the center position.

        Returns:
            True if a 3x3 open area exists, else False.
        """
        for dir in self.DIRS:
            if (self._is_in_bounds(x + dir[0] + 1, y + dir[1])
                and (self.grid[y + dir[1]][x + dir[0]] & 2
                     or self.grid[y + dir[1]][x + dir[0]] & 4)):
                return False
        return True

    def solve(self) -> List[str]:
        """Solve the maze using BFS and return the shortest path.

        Returns:
            List of directions as strings (N, E, S, W).
        """
        queue: Deque[Tuple[int, int]] = deque()
        queue.append(self.entry)
        visited: Set[Tuple[int, int]] = {self.entry}
        came_from: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}
        while True:
            curr: Tuple[int, int] = queue.popleft()
            if curr == self.exit:
                break
            for dir in self.DIRS:
                next: Tuple[int, int] = (curr[0] + dir[0], curr[1] + dir[1])
                if (self._is_in_bounds(*next) and next not in visited
                        and self.grid[curr[1]][curr[0]] & dir[2] == 0):
                    queue.append(next)
                    visited.add(next)
                    came_from[next] = (curr, dir[4])
        self.path = []
        while curr != self.entry:
            prev, nesw = came_from[curr]
            self.path.append(nesw)
            curr = prev
        self.path.reverse()
        return self.path
