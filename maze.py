from typing import List

BLOCKED = -1
FOUR: List[tuple] = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4)]
TWO: List[tuple] = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2),
                    (0, 3), (0, 4), (1, 4), (2, 4)]


class MazeGenerator:
    """Geneates a maze using the backtracker algorithm."""

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
                row.append(0)
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
