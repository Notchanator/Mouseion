# Mouseion — Claude Context

This is a personal project repository named after the Mouseion of Alexandria, housing larger personal projects across Python, Java, and R.

---

## Repository Structure

```
Mouseion/
├── GeniusStar/          # Python/Pygame — digital implementation of the Genius Star puzzle game
├── Wordle/              # Python — Wordle game implementation + solver + data analysis
├── Chess/               # Java — chess game with GUI
├── Rush Hour/           # Java — Rush Hour sliding puzzle game with GUI
├── Color Simplifier/    # Python — image color reduction using clustering (K-means)
└── Spotify Playlist Creator/  # R — Spotify data analysis and playlist generation
```

---

## Projects

### GeniusStar (`GeniusStar/`)
A 2-player competitive puzzle game where 7 dice dictate obstacle placement on a star-shaped board of 48 triangles, and players race to fill all spaces with 12 pieces.

- **Stack:** Python, Pygame, Shapely
- **Entry point:** `App/main.py`
- **Run locally:** `source /Users/notchjohnson/Mouseion/Mouseion/GeniusStar/.venv/bin/activate`
- **Active tasks:**
  - Draw picked-up pieces first (before others)
  - Detect when the board is successfully solved
  - Create a start screen with dice roll display
  - Add help UI for piece movement
  - Refactor: abstract Board to inherit Piece class
  - Refactor: piece placement check logic
  - Implement a fastest-solver algorithm
  - Improve exhaustive solver (OOP, parallel processes)

### Wordle (`Wordle/`)
Wordle game with a solver and data exploration notebook.

- **Stack:** Python
- **Key files:** `wordle.py`, `playWordle.py`, `solveWordle.py`, `dataExploration.ipynb`
- **Data:** `wordle_answers.csv`, `wordle_guesses.csv`

### Chess (`Chess/`)
Chess game with a Java Swing GUI.

- **Stack:** Java
- **Source:** `src/` — piece classes (Knight, Rook, Bishop, Queen, King, Pieces), Board, VirtualWorld, Images, Loading

### Rush Hour (`Rush Hour/`)
Rush Hour sliding puzzle implementation.

- **Stack:** Java
- **Structure mirrors Chess** — `src/` with game logic, `boards/` for puzzle configs, `images/` for assets

### Color Simplifier (`Color Simplifier/`)
Reduces images to a simplified color palette using clustering algorithms.

- **Stack:** Python
- **Key files:** `ColorSimplifier.py`, `Kmeans.py`, `Application.py`, `Helpers.py`

### Spotify Playlist Creator (`Spotify Playlist Creator/`)
R-based Spotify data analysis and automated playlist generation.

- **Stack:** R (R Markdown notebooks)
- **Key files:** `The Stuff/Playlist Creator.Rmd`, `Data Cleaning.Rmd`, `Data Creator.Rmd`

---

## Branch Naming Convention

Branches are scoped per project using the format `{Project}-{Purpose}`:

| Project              | Shorthand |
|----------------------|-----------|
| Mouseion (repo-wide) | M         |
| GeniusStar           | GS        |
| Wordle               | W         |

Example: `GS-solver-refactor`, `W-entropy-fix`, `M-readme-update`

---

## Notes for Claude

- Python projects use local virtual environments (`.venv/` or `venv/`) — activate before running
- Java projects use IntelliJ IDEA (`.idea/`, `.iml` files present) — do not modify IDE config files
- Avoid committing `.DS_Store`, `__pycache__/`, `.RData`, `.httr-oauth`, or `.Rhistory` files (see `.gitignore`)
- Each project is largely self-contained — changes in one project should not affect others
- GeniusStar is the most actively developed project
