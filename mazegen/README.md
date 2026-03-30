# mazegen

A Python maze generation package using recursive backtracking.

## Usage
```python
from mazegen import MazeGenerator

config = {"width": 20,
          "height": 15,
          "entry": (0, 0),
          "exit": (19, 14),
          "output_file": "maze.txt",
          "perfect": True}

maze = MazeGenerator(**config)
maze.generate_maze()
maze.solve()
```

## Optional Parameters
```python
# With seed for reproducibility
config["seed"] = 42

# With 42 pattern (min 11x9)
config["pattern"] = True
```

## Accessing the maze
```python
# Access the generated maze grid
maze.grid

# Access the solution
maze.path
```
