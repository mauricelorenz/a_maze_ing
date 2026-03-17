*This project has been created as part of the 42 curriculum by mlorenz, lemmerli.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It generates random mazes using the
recursive backtracker algorithm, displays them visually in the terminal, and writes the
result to an output file. The maze can be perfect (exactly one path from entry to exit)
or non-perfect (multiple paths). A "42" pattern is embedded in the maze as fully closed
cells.

## Instructions

### Requirements
- Python 3.10 or later
- A virtual environment is recommended

### Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

### Running
```bash
make run
```

Or with a custom config file:
```bash
python3 a_maze_ing.py my_config.txt
```

### Other commands
```bash
make lint        # Run flake8 and mypy
make debug       # Run with pdb debugger
make clean       # Remove cache files
```

## Config File

The config file uses KEY=VALUE pairs, one per line. Lines starting with `#` are comments.

| Key | Description | Required | Example |
|-----|-------------|----------|---------|
| WIDTH | Maze width in cells | Yes | `WIDTH=20` |
| HEIGHT | Maze height in cells | Yes | `HEIGHT=15` |
| ENTRY | Entry coordinates (x,y) | Yes | `ENTRY=0,0` |
| EXIT | Exit coordinates (x,y) | Yes | `EXIT=19,14` |
| OUTPUT_FILE | Output filename | Yes | `OUTPUT_FILE=maze.txt` |
| PERFECT | Perfect maze? (True/False) | Yes | `PERFECT=True` |
| SEED | Random seed for reproducibility | No | `SEED=12345678` |
| PATTERN | Show 42 pattern? (True/False) | No | `PATTERN=True` |

## Algorithm

We chose the **Recursive Backtracker** algorithm (randomized DFS). It works by:
1. Starting at the entry cell
2. Randomly visiting unvisited neighbors and removing walls
3. Backtracking when no unvisited neighbors remain
4. Repeating until all cells are visited

**Why this algorithm?**
- Simple to understand and implement
- Automatically guarantees full connectivity — no isolated cells
- Always produces a perfect maze by default
- Seed-based reproducibility is trivial to add
- Works naturally with our hexadecimal wall representation

For non-perfect mazes, ~10% of additional walls are randomly removed to create loops,
and a second opening at the entry is guaranteed.

## Visual Representation

The maze is rendered in the terminal using Unicode block characters. Colors:
- White: walls
- Green: entry
- Red: exit
- Blue: 42 pattern cells
- Yellow: solution path

### User interactions
1. Re-generate a new maze
2. Show/Hide shortest path from entry to exit
3. Rotate wall colors
4. Quit

## Reusable Module (mazegen)

The maze generation logic is available as a standalone pip-installable package.

### Installation
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or in development mode:
```bash
pip install -e .
```

### Basic Example
```python
from mazegen import MazeGenerator

config = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (19, 14),
    "PERFECT": True,
    "PATTERN": False
}

maze = MazeGenerator(config)
maze.generate_maze()
path = maze.solve()

print(maze.grid)   # 2D list with wall values as hex integers
print(path)        # ['N', 'E', 'S', ...] shortest path
```

### Custom Parameters
```python
# With seed for reproducibility
config["SEED"] = 42

# Non-perfect maze with 42 pattern
config["PERFECT"] = False
config["PATTERN"] = True
```

### Accessing the maze structure
- `maze.grid` — 2D list of integers, each cell encodes its walls as a 4-bit hex value
- `maze.path` — list of directions (N/E/S/W) representing the shortest path
- `maze.width` / `maze.height` — dimensions of the maze

### Building the package
```bash
pip install build
python -m build
```

## Team & Project Management

### Roles
- **lemmerli**: Config parser, maze grid structure, 42 pattern, BFS pathfinding, refactoring, package structure
- **mauricelorenz**: Config parser, Recursive backtracker algorithm, output file generation, terminal rendering

### Planning
We started by understanding the hex wall representation and the recursive backtracker algorithm,
then built the config parser, maze generator, pathfinding and rendering incrementally.
The main challenge was the non-perfect maze generation — ensuring multiple paths while
respecting the 3x3 open area constraint required several iterations.

### What worked well
- Splitting into separate modules made the code clean and testable
- The recursive backtracker was straightforward to implement
- BFS pathfinding reused the same direction logic as the generator

### What could be improved
- The `MazeGenerator` class still accepts a project-specific config dict — a cleaner
  API with individual parameters would make it more reusable
- More test coverage for the maze generation and pathfinding

### Tools used
- VS Code with Python extension
- Claude AI for guidance on algorithms, debugging and code structure
- Git/GitHub for version control

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracking — Jamis Buck](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Maze generation visualizations](https://professor-l.github.io/mazes/)
- [Maze Generator in Python — inventwithpython.com](https://inventwithpython.com/recursion/chapter11.html)

### AI Usage
Claude AI was used throughout the project for:
- Explaining algorithms (recursive backtracker, BFS, spanning trees)
- Debugging logic errors (3x3 check, non-perfect path guarantee)
- Code structure and refactoring advice

All generated suggestions were reviewed, understood and adapted before use.