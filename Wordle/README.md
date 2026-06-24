# Wordle

Wordle is a word puzzle game released in 2021 — so popular it was acquired by the New York Times. Each day has a secret 5-letter word that players try to guess in 6 attempts, receiving color-coded feedback after each guess (green = correct position, yellow = wrong position, grey = not in word).

This project has three components: a playable game, a solver bot, and data analysis that informed the bot's strategy.

---

## Project Structure

```
Wordle/
├── src/
│   ├── wordle.py          # Core Wordle class — shared game logic
│   ├── playWordle.py      # Tkinter GUI — playable, repeatable Wordle app
│   └── solveWordle.py     # CLI solver assistant
├── data/
│   ├── wordle_answers.csv # Valid answer words (~2,300 words)
│   ├── wordle_guesses.csv # All valid guess words (~13,000 words)
│   └── winning_messages.csv
├── scripts/
│   └── word-scraper.py    # One-time utility used to build word lists
├── notebooks/
│   └── dataExploration.ipynb  # Letter frequency and entropy analysis
├── outputs/               # Generated analysis files (gitignored)
└── docs/
    └── Analysis.pages     # Analysis writeup
```

---

## Running Locally

Dependencies are managed with [uv](https://docs.astral.sh/uv/) via `pyproject.toml`.

```bash
# One-time: install uv — https://docs.astral.sh/uv/getting-started/installation/
brew install uv

# From the Wordle/ directory — creates .venv and installs the locked deps
cd Wordle
uv sync                 # runtime deps only
uv sync --all-groups    # also installs the Jupyter dev tooling

# Run anything in the managed environment with `uv run` (no manual activation)
uv run python src/playWordle.py   # playable GUI game
uv run python src/solveWordle.py  # CLI solver assistant
uv run jupyter lab                # data-analysis notebook
```

`uv run` resolves and uses the project's `.venv` automatically, so there's no `source .venv/bin/activate` step. Commit `pyproject.toml`, `uv.lock`, and `.python-version`; `.venv/` is gitignored.

---

## Playable Game

A Tkinter desktop app that replicates the Wordle experience with unlimited replays. Tracks win/loss statistics across sessions within a single run.

- Type letters to fill a tile row, Backspace to delete, Enter to submit
- Tiles color green/yellow/grey after each guess
- The keyboard display at the bottom tracks known letter states
- Click anywhere to start a new game after the round ends

---

## Wordle Bot

`solveWordle.py` is a CLI assistant for use alongside the real NYT Wordle. It accepts your existing guesses and their scores, then recommends the next guess using information theory (entropy maximization).

**Usage:**

```
Number of guesses already done: 1
Guess: crane
Input Scores like 01021. Where 1 represents Yellow and 2 represents Green.
Score: 00010
Suggested Word: slimy
```

Scoring format: one digit per letter — `0` grey, `1` yellow, `2` green.

---

## Data Analysis

The notebook (`notebooks/dataExploration.ipynb`) explores the structure of the Wordle answer list and derives the bot's opening strategy.

**Letter frequency analysis** — charts the distribution of each letter across all 5 positions in the answer set, identifying which letters and positions are most information-rich.

**Entropy-based word ranking** — scores every valid guess word by its expected information gain (Shannon entropy) against the full answer set. A higher-entropy guess splits the remaining possibilities more evenly, converging on the answer faster.

**Bot performance** — the bot was tested against all ~2,300 possible answers. Top opening words by entropy:

| Word  | Mean Guesses |
|-------|-------------|
| soare | 3.49        |
| raise | 3.49        |
| roate | 3.49        |

The bot solves all tested answers within 6 guesses, with most games resolved in 3–4.
