# GeniusStar — Claude Context

A Python/Pygame digital implementation of the [Genius Star](https://www.smartgames.eu/uk/one-player-games/genius-star.html) puzzle game — a 2-player competitive puzzle where 7 dice determine obstacle placement on a star-shaped board of 48 triangles, and players race to fill all spaces with 12 pieces (11 unique shapes).

---

## Project Structure

```
GeniusStar/
├── App/
│   ├── main.py        # Entry point — Pygame loop, event handling, rendering
│   ├── setup.py       # Setup class — builds board, pieces, obstacles; orchestrates game start
│   ├── board.py       # Board class — triangle geometry, board state
│   ├── piece.py       # Piece class — triangle-based shapes, movement, display
│   ├── obstacle.py    # Obstacle class — fixed board blockers from dice rolls
│   └── config.py      # Config class — piece colors, starting positions, dice face values
├── Resources/
│   ├── Board.csv      # Triangle vertex coordinates for all 48 board spaces
│   └── GamePieces/    # CSVs defining triangle compositions of each piece
├── Development.ipynb  # Jupyter notebook for prototyping and solver development
├── .venv/             # Virtual environment (use this one)
└── venv/              # Older venv (prefer .venv)
```

---

## Architecture

### Key Classes

**`Config`** (`config.py`)
- Defines piece colors (RGB) and initial screen positions
- `createDice()` returns 7 lists of triangle IDs, one per die face — dice rolls index into these

**`Setup`** (`setup.py`)
- Orchestrates game initialization: `buildBoard()`, `buildPieces()`, `applyPieceConfig()`
- `playGame()` rolls dice and returns `(board, pieces, obstacles)`
- Pieces are loaded from `Resources/GamePieces/*.csv`

**`Board`** (`board.py`)
- Loads triangle geometry from `Resources/Board.csv`
- Each triangle has vertex coordinates (`v1_x`, `v1_y`, `v2_x`, `v2_y`, `v3_x`, `v3_y`)

**`Piece`** (`piece.py`)
- Triangle-based shapes using Shapely `Polygon` for hit detection
- `createShapelyTriangle()` converts a data row to a Shapely polygon
- `calculateCenter()` gets triangle centroid for display/movement

**`main.py`**
- Pygame event loop
- `isClickOnPiece()` uses barycentric coordinates for hit detection
- `distanceBetweenTriangles()` handles piece drag movement

---

## Running Locally

```bash
source /Users/notchjohnson/Mouseion/Mouseion/GeniusStar/.venv/bin/activate
cd Mouseion/GeniusStar/App
python main.py
```

Dependencies: `pygame`, `shapely`, `pandas`, `numpy`

---

## Active Development Tasks

### Game Movement
- Draw picked-up pieces first (before stationary pieces) during rendering

### Game Mechanics
- Detect when the board is successfully solved (all 48 triangles covered)

### Game UI
- Create a start screen that displays dice roll results
- Add a help UI for piece movement controls

### Code Improvements
- Abstract `Board` class to inherit from `Piece` class (shared triangle logic)
- Refactor piece placement check logic

### Solver
- Implement first iteration of a fastest-solver algorithm
- Improve exhaustive solver: convert to OOP, add parallel processes for speed

---

## Notes for Claude

- Run scripts from `App/` directory so relative paths to `Resources/` resolve
- Prefer `.venv/` over `venv/` — `.venv` is the current environment
- Triangle IDs are 1-indexed (1–48) matching `Board.csv` row labels
- Piece files in `Resources/GamePieces/` are named by color + triangle count (e.g. `DarkGreen5.csv`, `Yellow2.csv`)
- `Development.ipynb` is the prototyping scratchpad — solver work lives there
- Do not modify `.venv/` or `venv/` contents directly
