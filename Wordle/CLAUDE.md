# Wordle — Claude Context

A Python implementation of Wordle with three components: a playable game, a solver bot, and data analysis.

---

## Project Structure

```
Wordle/
├── wordle.py              # Core Wordle class — game logic, word evaluation, word bank tracking
├── playWordle.py          # Tkinter GUI — playable, repeatable Wordle app
├── solveWordle.py         # CLI solver bot — entropy-based word suggester (separate Wordle class, TODO: merge)
├── word-scraper.py        # Scraper to build word lists
├── dataExploration.ipynb  # Jupyter notebook — letter frequency and entropy analysis
├── wordle_answers.csv     # Valid answer words
├── wordle_guesses.csv     # All valid guess words
└── Outputs/               # Analysis output files (CSVs, PNGs)
```

---

## How It Works

### Core (`wordle.py`)
- `Wordle` class manages game state: word bank (letter status tracking), turn counter, guess validation
- `evaluateGuess()` scores a guess: green (correct position), yellow (wrong position), grey (not in word)
- Word bank uses `-1` (unknown), `0` (grey), `1` (yellow), `2` (green) per letter
- Words loaded via `np.loadtxt` — run from the `Wordle/` directory so relative CSV paths resolve

### Playable Game (`playWordle.py`)
- Tkinter `App` canvas class — wraps `Wordle`, tracks stats across sessions
- Prints the answer to console on game start (debug)

### Solver (`solveWordle.py`)
- Standalone script — prompts for existing guesses + scores, then suggests next guess by entropy
- Has its own `Wordle` class (duplicate of core — TODO: refactor into one)
- Scoring format: word + score string, e.g. `"apple" "10021"` where 0=grey, 1=yellow, 2=green

---

## Running Locally

Run from within the `Wordle/` directory so CSV paths resolve correctly:

```bash
cd Mouseion/Wordle
python playWordle.py   # GUI game
python solveWordle.py  # CLI solver
```

Dependencies: `numpy`, `pandas`, `tkinter` (stdlib)

---

## Known Issues / Active Work

- `solveWordle.py` has a duplicate `Wordle` class — should be refactored to import from `wordle.py`
- `word-scraper.py` may need updating if word source changes
- Data Analysis section in README is currently empty — `dataExploration.ipynb` contains the work

---

## Notes for Claude

- Keep file paths relative; scripts expect to be run from `Wordle/`
- The word bank dict in `Wordle.__init__` uses `-1` as "unseen" (not `None` or `False`)
- Don't modify `wordle_answers.csv` or `wordle_guesses.csv` without good reason — they're the source of truth for valid words
- `__pycache__/` is gitignored; ignore it
