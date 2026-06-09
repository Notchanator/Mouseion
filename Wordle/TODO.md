# Wordle — To Do

### Bugs
- [ ] **`solveWordle.py` — `turn` increments crash on init** (`wordle.py:38`): `for word in usedWords: turn += 1` references the class-level `turn` without `self.`, causing an `UnboundLocalError` at runtime when `usedWords` is non-empty
- [ ] **`solveWordle.py` — mutable default arguments** (`wordle.py:34`): `def __init__(self, usedWords=[], usedWordsScore=[])` uses mutable defaults — list state persists across instantiations; replace with `None` and assign inside the method
- [ ] **`solveWordle.py` — `wordBank` is a class-level attribute** (`wordle.py:32`): defined on the class, not per-instance, so all `Wordle` instances share the same word bank dict and mutations to one affect all others
- [ ] **`solveWordle.py` — score instructions print on wrong guess** (`solveWordle.py:90`): `if guess == 1` should be `if guess == 0` — the scoring format instructions only print before the second guess input, not the first
- [ ] **`solveWordle.py` — absolute hardcoded paths** (`solveWordle.py:29-30`): data files are loaded with hardcoded absolute paths (e.g. `/Users/notchjohnson/...`), unlike `wordle.py` and `playWordle.py` which use `pathlib`; update to use `_DATA_DIR`
- [x] **`wordle.py` — program body runs on import** (`wordle.py:94-98`): the `while True` game loop at the bottom of `wordle.py` executes when the module is imported by `playWordle.py`; should be guarded with `if __name__ == "__main__":`

### Refactoring
- [ ] **Merge duplicate `Wordle` classes** — `solveWordle.py` defines its own `Wordle` class that duplicates `wordle.py`; refactor `solveWordle.py` to import and extend the shared class
- [ ] **`solveWordle.py` — `subsetAllWords` is a no-op** (`solveWordle.py:48-62`): all three branches (`grey`, `yellow`, `green`) are `pass` — the core filtering logic still needs to be implemented
- [ ] **`solveWordle.py` — `suggestWord` is a stub** (`solveWordle.py:73-75`): always returns `"Apple"`; needs entropy-based implementation modelled on the notebook's `wordleBot`
- [ ] **`solveWordle.py` — `createAnswersDF` is a stub** (`solveWordle.py:41-44`): returns a bare `pd.DataFrame(numpyList)` with no column splitting per letter position

### Tasks
- [ ] **Improve Play Wordle UI**: Add ? to add rules and key binds. Add functionality for next game. Add functionality to give up.
- [ ] **Implement Statistics Functionality**: Move statistics from a text output to a UI element. 

### Minor
- [ ] **`playWordle.py` — answer printed to console on game start** (`playWordle.py:28`): `print(self.wordle.theWord)` is a debug leftover; remove before treating the app as releasable
- [ ] **`wordle.py` — `printCorrectLetters` / `printSemiCorrectLetters` call undefined methods** (`wordle.py:66-73`): both call `self.findCorrectLetters()` and `self.findSemiCorrectLetters()` which are never defined anywhere in the class

## Done
- [x] Restructure project folders (`src/`, `data/`, `scripts/`, `notebooks/`, `docs/`)
- [x] Fill out README
