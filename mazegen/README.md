# mazegen

A Python maze generation package using the recursive backtracker algorithm.

## Installation
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic Example
```python
from mazegen import MazeGenerator

config = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (19, 14),
    "PERFECT": True
}

maze = MazeGenerator(config)
maze.generate_maze()
path = maze.solve()
```

## Custom Parameters
```python
# With seed for reproducibility
config["SEED"] = 42

# Non-perfect maze
config["PERFECT"] = False

# With 42 pattern (min 11x9)
config["PATTERN"] = True
```

## Accessing the maze
```python
maze.grid    # 2D list of integers, walls encoded as 4-bit hex values
maze.path    # ['N', 'E', 'S', ...] shortest path from entry to exit
maze.width   # maze width
maze.height  # maze height
```

## Wall encoding

Each cell value is a 4-bit integer:

| Bit | Wall |
|-----|------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

`1` = wall closed, `0` = wall open. Example: `15` (binary `1111`) = all walls closed.