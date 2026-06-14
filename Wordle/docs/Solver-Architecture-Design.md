# Wordle Solver — Architecture Design Document

## Overview

This document settles how the solver (`solveWordle.py`) should be structured relative to
the playable game (`playWordle.py` / `wordle.py`), and lays out the target architecture for
completing the solver.

The central question: the game and the solver are *opposite* use-cases —

- **Game (host role):** we pick a secret word and **evaluate** the player's guesses against it.
- **Solver (guesser role):** we don't know the word; we **suggest** guesses, the player reports
  the evaluation, and we narrow the candidate set until one word remains.

Should these be two separate classes, or one shared class?

---

## The Decision: Two Role Classes on One Shared Scoring Kernel

Neither extreme is right.

- **Not one class.** The state is genuinely disjoint. The host owns a *secret answer*; the
  solver owns a *shrinking candidate set*. A single class would leave half its attributes
  meaningless in each mode (`theWord` is nonsense to a solver; a candidate set is nonsense to a
  host). Single-responsibility says keep them apart: the host's job is to *hide and reveal*, the
  solver's job is to *infer*.

- **Not two independent classes (the status quo).** Today `solveWordle.py` defines its own
  duplicate `Wordle` class. That duplication is the actual risk, because the two roles share
  exactly one thing that **must stay identical**: the scoring rule
  `evaluateGuess(guess, answer)`. The host uses it to score the player. The solver uses it to
  reason about *hypothetical* answers — "if the true word were X, what evaluation would this
  guess produce?" — which is the entire basis of candidate subsetting and entropy. If the two
  copies of the scoring rule ever drift, the solver silently computes against the wrong game.

So: **one stateless scoring kernel, two stateful role classes that sit on top of it.**

```
                  scoring.py  (stateless, pure)
                  - evaluateGuess(guess, answer)
                  - word-list loading
                        ▲                ▲
                        │                │
              Wordle (host)        WordleSolver
              wordle.py            solveWordle.py
              owns: theWord        owns: candidate set
              evaluates guesses    suggests guesses,
              for playWordle.py    subsets on reported scores
```

The scoring rule is the *contract* between the two roles, and it lives in exactly one place.

---

## Shared Kernel — `scoring.py` (new)

A new, dependency-light module (no tkinter, no game/solver state). Both role classes import it.

| Function | Responsibility |
|---|---|
| `evaluateGuess(guess, answer)` | The canonical scoring rule. Returns the per-letter score list `[[letter, code], ...]` where `code` is `0` grey / `1` yellow / `2` green. This is the existing `wordle.py` algorithm, lifted out as a **pure function** of two strings. |
| `encode(score) -> "10221"` | Collapses the score list into the compact string the solver reasons with (and that the player types in). One canonical representation, one encoder — no second copy of the logic. |
| `load_words(path) -> np.ndarray` | Thin `np.loadtxt` wrapper so both roles load word lists the same way, via `conf.DATA`. |

Why a *new* module rather than importing from `wordle.py`: it keeps the solver from depending
on the game module (which is tkinter-adjacent) and matches this project's small-module style
(`toolbar.py`, `buttons.py`, `dialogs.py`, `keyboard.py`, `util.py`).

> **Note on the two encodings.** The game needs the `[[letter, code]]` form to colour tiles and
> update the keyboard; the solver needs the `"10221"` string to group answers by outcome. These
> are two encodings of *one* result. The kernel produces the list form (what the game already
> expects, so the game barely changes) and offers `encode()` for the solver. They never diverge.

---

## Game Host — `Wordle` (`wordle.py`, mostly unchanged)

Stays the class it already is. The only change: its `evaluateGuess` method becomes a thin
delegate so the host and solver share one rule.

```python
def evaluateGuess(self):
    return scoring.evaluateGuess(self.userWord, self.theWord)
```

Public API (`playGame`, `testUserWord`, `updateWordBank`, `theWord`, `finished`, `wordBank`, …)
is untouched, so **`playWordle.py` does not change at all.**

---

## Solver — `WordleSolver` (`solveWordle.py`, rewritten)

A new class replacing the duplicate `Wordle` class and its stubbed methods. CLI-only: the class
holds the inference logic with **zero I/O**, and a small `main()` loop at the bottom does the
prompting. (Keeping I/O out of the class costs nothing now and leaves the door open later, but
we are not building any GUI integration.)

### State

| Attribute | Meaning |
|---|---|
| `candidates` | `np.ndarray` of the still-possible answer words. Starts as the full answer list, shrinks each turn. |
| `turn` | Guess counter, starts at 0. |

Notably **absent:** `theWord` (we don't know it) and `wordBank` (the per-letter status dict is a
game/keyboard concern — the solver reasons over whole-word evaluation patterns, not letter
status, so it doesn't need it). Dropping `wordBank` here also dissolves three open TODO bugs at
once (class-level `wordBank`, mutable default args, `turn += 1` without `self`).

### Methods

| Method | Responsibility |
|---|---|
| `suggest() -> str` | Turn 0 → return the **hardcoded opener** (see below). Otherwise compute entropy live over the current `candidates` and return the highest-information word. |
| `record(guess, code)` | Subset `candidates` to those answers `a` where `encode(evaluateGuess(guess, a)) == code`; increment `turn`. This is the inference step — "keep only the words consistent with what the player just reported." |
| `_entropy(guess) -> float` | (private) Partition remaining `candidates` by the evaluation `guess` would produce against each; `H = -Σ pᵢ log₂ pᵢ` over partition sizes. |
| `solved` (property) | `len(candidates) == 1`. |

### Why a hardcoded opener

Computing first-guess entropy over the full word list from scratch is the expensive case
(~15 min in the notebook). The opener is the *same every game*, so we hardcode it (e.g. `soare`,
matching the notebook) and only compute live from turn 2 onward — by which point the candidate
set has collapsed and entropy is cheap. This is what makes "compute live, no precomputed
cross-table" practical. The opener belongs in `conf.py` as a constant
(e.g. `SOLVER = {"opener": "soare"}`), matching how the rest of the config lives there.

### What this replaces

The current `subsetAllWords` (empty `pass` branches doing letter-by-letter filtering),
`createAnswersDF`, and the always-`"Apple"` `suggestWord` stub are all superseded by the
`record` / `suggest` / `_entropy` trio above, which mirror the notebook's `subsetAnswers` +
`wordleBot` — but computed live instead of from the cross-table.

---

## Data Flow (Solver CLI)

```
main() loop:
  guess = solver.suggest()          # turn 0 → opener; else best live-entropy word
  print("Suggested:", guess)
  code  = input("Score (e.g. 10221, or 'done'): ")
  if code == 'done': break          # the suggestion was the answer
  solver.record(guess, code)        # candidates shrink to those consistent with `code`
  if solver.solved:                 # one word left
      print("Answer:", solver.candidates[0]); break
```

The player is the oracle: the solver proposes, the player reports the real game's evaluation,
and the solver uses the **shared** `evaluateGuess` to keep only candidates that would have
produced that exact report.

---

## File Structure

```
src/
├── scoring.py       ← NEW: evaluateGuess (pure) + encode() + load_words()
├── wordle.py        ← Wordle host; evaluateGuess delegates to scoring (otherwise unchanged)
├── playWordle.py    ← unchanged
├── solveWordle.py   ← WordleSolver class + main() CLI loop (rewritten; no duplicate Wordle class)
└── conf.py          ← add SOLVER = {"opener": "soare"}; DATA paths reused
```

---

## What Stays the Same

- `playWordle.py` and the whole tkinter UI layer — untouched.
- The `Wordle` host class's public API and game behaviour — unchanged; only the *body* of
  `evaluateGuess` moves into `scoring.py`.
- `conf.DATA` remains the single source of word-list paths (this also fixes the solver's
  hardcoded absolute paths — TODO item).
- The word-data files themselves (`wordle_answers.csv`, `wordle_guesses.csv`).

---

## Resolved Decisions

- **Opener: `soare`** — hardcoded as `conf.SOLVER["opener"]`. It's the same every game, so turn 1
  never pays the full-list entropy cost. Easy to swap later (one constant).
- **Subset-before-entropy** — entropy is *only ever* computed over the surviving candidate set,
  never the full word list. `record()` shrinks `candidates` first; `suggest()` then scores
  entropy across those survivors (each survivor is also a candidate guess). After turn 1 the set
  has collapsed, so the O(n²) entropy pass is cheap. This is the key run-time win: we pay
  information-theory cost proportional to *what's left*, not to the whole dictionary.
