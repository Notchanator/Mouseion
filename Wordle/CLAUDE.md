# Wordle — Claude Context

A Python implementation of Wordle with three components: a playable game, a solver bot, and data analysis.

---

## Project Structure

```
Wordle/
├── src/
│   ├── wordle.py          # Core Wordle class — game logic, word evaluation, word bank tracking
│   ├── playWordle.py      # Tkinter GUI — playable, repeatable Wordle app
│   └── solveWordle.py     # CLI solver bot — entropy-based word suggester (separate Wordle class, TODO: merge)
├── data/
│   ├── wordle_answers.csv # Valid answer words
│   ├── wordle_guesses.csv # All valid guess words
│   └── winning_messages.csv
├── scripts/
│   └── word-scraper.py    # One-time utility to build word lists
├── notebooks/
│   └── dataExploration.ipynb  # Letter frequency and entropy analysis
├── outputs/               # Generated analysis files (gitignored)
└── docs/
    └── Analysis.pages     # Analysis writeup
```

---

## How It Works

### Core (`src/wordle.py`)
- `Wordle` class manages game state: word bank (letter status tracking), turn counter, guess validation
- `evaluateGuess()` scores a guess: green (correct position), yellow (wrong position), grey (not in word)
- Word bank uses `-1` (unknown), `0` (grey), `1` (yellow), `2` (green) per letter
- Data paths resolved via `pathlib` relative to `src/` — scripts can be run from any directory

### Playable Game (`src/playWordle.py`)
- Tkinter `App` canvas class — wraps `Wordle`, tracks stats across sessions
- Prints the answer to console on game start (debug)

### Solver (`src/solveWordle.py`)
- Standalone script — prompts for existing guesses + scores, then suggests next guess by entropy
- Has its own `Wordle` class (duplicate of core — TODO: refactor into one)
- Scoring format: word + score string, e.g. `"apple" "10021"` where 0=grey, 1=yellow, 2=green

---

## Running Locally

Dependencies are managed with [uv](https://docs.astral.sh/uv/) via `pyproject.toml` + `uv.lock`. 

Use `uv run` from the `Wordle/` directory — no manual `.venv` activation. 

```bash
uv sync --all-groups               # set up .venv from the lockfile (incl. Jupyter)
uv run python src/playWordle.py    # GUI game
uv run python src/solveWordle.py   # CLI solver
```

---

## Known Issues / Active Work

- `solveWordle.py` has a duplicate `Wordle` class — should be refactored to import from `wordle.py`
- `word-scraper.py` may need updating if word source changes
- Data Analysis section in README is currently empty — `dataExploration.ipynb` contains the work

---

## Notes for Claude

- Data paths use `pathlib` (`_DATA_DIR = Path(__file__).parent.parent / "data"`) — no need to run from a specific directory
- The word bank dict in `Wordle.__init__` uses `-1` as "unseen" (not `None` or `False`)
- Don't modify `data/wordle_answers.csv` or `data/wordle_guesses.csv` without good reason — they're the source of truth for valid words
- `outputs/` is gitignored — generated files go there
