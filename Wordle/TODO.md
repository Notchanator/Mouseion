# Wordle — To Do

### Bugs
- [x] **`solveWordle.py` — `turn` increments crash on init**: resolved by the `WordleSolver` rewrite — the duplicate `Wordle` class is gone
- [x] **`solveWordle.py` — mutable default arguments**: resolved — `WordleSolver.__init__` takes no list defaults
- [x] **`solveWordle.py` — `wordBank` is a class-level attribute**: resolved — the solver no longer uses `wordBank` (a game/keyboard concern); state is per-instance `candidates`
- [x] **`solveWordle.py` — score instructions print on wrong guess**: resolved — the CLI loop now prints the score format once up front
- [x] **`solveWordle.py` — absolute hardcoded paths**: resolved — loads via `conf.DATA` / `scoring.load_words`
- [x] **`wordle.py` — program body runs on import** (`wordle.py:94-98`): the `while True` game loop at the bottom of `wordle.py` executes when the module is imported by `playWordle.py`; should be guarded with `if __name__ == "__main__":`

### Refactoring
- [x] **Merge duplicate `Wordle` classes** — resolved via `scoring.py`: the scoring rule + word loading now live in one stateless kernel that both `wordle.py` (host) and `solveWordle.py` (`WordleSolver`) import. See `docs/Solver-Architecture-Design.md`
- [x] **`solveWordle.py` — `subsetAllWords` is a no-op**: resolved — replaced by `WordleSolver.record`, which subsets candidates by reported score using the shared `evaluateGuess`
- [x] **`solveWordle.py` — `suggestWord` is a stub**: resolved — `WordleSolver.suggest` returns the `soare` opener then live highest-entropy survivors
- [x] **`solveWordle.py` — `createAnswersDF` is a stub**: resolved — removed; the cross-table-free `record`/`_entropy` design doesn't need it

### Tasks
- [ ] **Improve Play Wordle UI**: Add ? to add rules and key binds. Add functionality for next game. Add functionality to give up.
- [ ] **Implement Statistics Functionality**: Move statistics from a text output to a UI element. 

### Minor
- [ ] **`playWordle.py` — answer printed to console on game start** (`playWordle.py:28`): `print(self.wordle.theWord)` is a debug leftover; remove before treating the app as releasable
- [ ] **`wordle.py` — `printCorrectLetters` / `printSemiCorrectLetters` call undefined methods** (`wordle.py:66-73`): both call `self.findCorrectLetters()` and `self.findSemiCorrectLetters()` which are never defined anywhere in the class

## Done
- [x] Restructure project folders (`src/`, `data/`, `scripts/`, `notebooks/`, `docs/`)
- [x] Fill out README
