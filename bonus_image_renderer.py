"""Bonus: a_maze_ing module for image generation."""

from typing import List, Tuple, Dict
from PIL import Image, ImageDraw
from mazegen import MazeGenerator


def render_image(maze: MazeGenerator, rendered_maze: List[List[int]]) -> None:
    """Render image representation of the maze.

    Args:
        maze: MazeGenerator instance containing the grid.
        rendered_maze: 2D list containing the pixel representation.
    """
    canvas_width: int = (len(rendered_maze[0]) + 2) * 20
    canvas_height: int = (len(rendered_maze) + 2) * 20
    pixel_color: Dict[int, Tuple[int, int, int]] = {1: (0, 0, 0),
                                                    2: (0, 128, 0),
                                                    3: (196, 0, 0),
                                                    4: (36, 114, 200),
                                                    5: (229, 229, 16)}
    img: Image.Image = Image.new("RGB", (canvas_width, canvas_height),
                                 (255, 255, 255))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    for r, row in enumerate(rendered_maze):
        for c, col in enumerate(row):
            top_left: Tuple[int, int] = (c * 20 + 20, r * 20 + 20)
            bot_right: Tuple[int, int] = (c * 20 + 39, r * 20 + 39)
            if pixel_color.get(col, None):
                draw.rectangle([top_left, bot_right], fill=pixel_color[col])
    try:
        img.save(f"{maze.output_file.removesuffix('.txt')}.png")
    except Exception:
        print("Error while saving image!")
    img.show()
