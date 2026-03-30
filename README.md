*This project has been created as part of the 42 curriculum by mlorenz, lemmerli.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It generates random mazes using recursive backtracking, renders them in the terminal, and writes the result to an output file. The maze can be perfect (exactly one path from entry to exit) or non-perfect (multiple paths). By default a "42" pattern is embedded in the maze as cells with all walls intact if sufficient space is available.

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

### Other Commands
```bash
make debug       # Run with pdb debugger
make clean       # Remove cache files
make lint        # Run flake8 and mypy
make lint-strict # Run flake8 and mypy with --strict flag
```

## Config File

The config file uses KEY=VALUE pairs, one per line. Lines starting with `#` are comments.
Keys are case-insensitive.

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

For non-perfect mazes, walls near the entry cell and approximately 10% of remaining walls are randomly removed to introduce loops.

## Visual Representation

The maze is rendered in the terminal using Unicode block characters. Colors:
- White: walls
- Green: entry
- Red: exit
- Blue: 42 pattern cells
- Yellow: solution path

### User Interactions
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Bonus: Show and save maze as PNG
5. Quit

## Reusable Module (mazegen)

A Python maze generation package using recursive backtracking.

### Usage
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

### Optional Parameters
```python
# With seed for reproducibility
config["seed"] = 42

# With 42 pattern (min 11x9)
config["pattern"] = True
```

### Accessing the maze
```python
# Access the generated maze grid
maze.grid

# Access the solution
maze.path
```

## Team & Project Management

### Roles
- **lemmerli**: Config parser, maze grid structure, 42 pattern, BFS pathfinding, package structure
- **mlorenz**: Recursive backtracker algorithm, output file generation, terminal rendering, PNG rendering
- **Both**: Refactoring — splitting into separate modules (config_parser, maze_renderer, file_output), migrating from config dict to individual parameters in MazeGenerator, lowercasing config keys, moving DIRS to class attribute, non-perfect maze improvements

### Planning
We started by understanding the hex wall representation and the recursive backtracker algorithm, then built the config parser, maze generator, pathfinding and rendering incrementally. The main challenge was the non-perfect maze generation — ensuring multiple paths while respecting the 3x3 open area constraint required several iterations.
During refactoring we cleaned up the codebase significantly — separating concerns into dedicated modules and making the MazeGenerator API cleaner and more reusable.

### What worked well
- Splitting into separate modules made the code clean and testable
- The recursive backtracker was straightforward to implement
- BFS pathfinding reused the same direction logic as the generator
- Migrating to individual parameters made MazeGenerator truly reusable

### What could be improved
- Additional tests for the maze generation and pathfinding
- Rendering with a graphics library

### Tools used
- VSCode
- Claude AI as per AI Usage
- Git/GitHub for version control

## Resources

- [Maze Generator in Python — inventwithpython.com](https://inventwithpython.com/recursion/chapter11.html)

### AI Usage
In this project's implementation the use of AI was limited to:

- discussing general implementation
- minor details, like the naming of variables
- generation of smaller code snippets
- proofreading commit messages and this README
