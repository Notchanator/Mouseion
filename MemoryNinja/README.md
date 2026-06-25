# MemoryNinja

A browser-based, mobile-friendly 1v1 memory card game. Players take turns
flipping cards arranged in a 3-5-5-3 grid, trying to find matching pairs. See
[docs/design.md](docs/design.md) for the full design.

## Status

**Phase 1 — single-device pass-and-play: complete and playable.** Python game
core, a thin FastAPI web layer, and a vanilla-JS browser frontend are all built
and verified end-to-end in a browser.

| Component | State |
|-----------|-------|
| `backend/models.py` — data shapes (`Card`, `Pile`, `Player`, `GameState`) | ✅ done |
| `backend/game.py` — game logic (deal, turn flow, matching, win detection) | ✅ done |
| `backend/themes/animals.py` — animal theme (16 pairs) | ✅ done |
| `backend/main.py` — FastAPI REST adapter around the core | ✅ done |
| `frontend/` — board, 3D card flip, scoreboard, overlay (vanilla JS modules) | ✅ done |
| `tests/` — unit + API tests | ✅ done (31 tests) |
| Real card artwork (PNGs) | ⏳ using emoji/CSS placeholders |

## Play

```sh
uv run uvicorn backend.main:app --reload
```

Then open <http://localhost:8000> and tap **New Game**. Append `?seed=N` to the
URL for a reproducible deal (useful for replays and testing). Art is emoji/CSS
placeholders — drop PNGs into `frontend/assets/themes/animals/` and update
`renderArt` in `frontend/card.js` to use real images.

**Turn feel:** the first tapped card flips up and stays up; tapping a second
pile flips it up too, both hold face-up together for 3 seconds, then resolve.
The two cards are offset in opposite diagonals so they're easy to tell apart,
and the scoreboard updates when the cards visually resolve (not on tap).

## Setup

Dependencies are managed with [uv](https://docs.astral.sh/uv/) (repo
convention).

```sh
uv sync          # install dependencies (creates .venv)
uv run pytest    # run the test suite

# Run the API server (frontend mounts at / once it exists)
uv run uvicorn backend.main:app --reload
```

## API

The server is a thin adapter over the game core — it holds no rules and never
exposes the faces of face-down cards. A card's identity comes back only in the
`move` of the tap that reveals it.

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/api/health` | Liveness + registered themes |
| `POST` | `/api/games` | Create a game → `{game_id, state}`. Body: `player1`, `player2`, `theme`, `seed` (all optional) |
| `GET`  | `/api/games/{id}` | Current public board state |
| `POST` | `/api/games/{id}/select/{pile}` | Tap a pile → `{move, state}`. First tap reveals; second resolves |

`state` exposes per-pile `{index, is_empty, count}` only. `move` carries the
revealed `card`, plus `matched` / `turn_passed` / `game_over` / `winner`.
Invalid taps return `400`; unknown game ids return `404`.

## Architecture notes

- **Game logic is pure.** `backend/game.py` has no web, UI, or timer code. A tap
  is resolved by `Game.select_pile(index)`, which returns a `MoveResult` the UI
  uses to drive animations. The 3-second card-flip is a frontend concern.
- **Determinism.** `Game(seed=...)` makes every deal reproducible, which is what
  keeps the logic unit-testable.
- **The deal guarantees split pairs.** The two cards of a pair always land in
  different piles. Cards never move between piles during play, so a pair sharing
  a pile could never be collected — splitting them keeps the "all 16 pairs
  collected" end state reachable. This isn't spelled out in the design doc but
  is required for the game to be winnable.
- **REST, not WebSocket, in Phase 1.** For single-device pass-and-play there is
  no second client to push to, so the design doc's WebSocket would add nothing
  here. Phase 2 (online multiplayer) adds a WebSocket endpoint in `main.py` that
  broadcasts state to both connected players — without touching the core.
- **Hidden information stays on the server.** Because the public state view
  exposes pile counts but not card faces, a client cannot inspect cards it
  hasn't legitimately revealed. This is a structural benefit of keeping the
  authoritative game on the server.

## Project layout

```
MemoryNinja/
├── backend/
│   ├── main.py              # FastAPI REST adapter (the web boundary)
│   ├── models.py            # data shapes
│   ├── game.py              # core game logic
│   └── themes/animals.py    # animal theme definitions
├── frontend/
│   ├── index.html           # app shell
│   ├── style.css            # layout, card faces, 3D flip
│   ├── app.js               # orchestration + turn timing
│   ├── board.js             # 3-5-5-3 grid rendering
│   ├── card.js              # card DOM + flip + placeholder art
│   └── gameState.js         # API client + mirrored state
├── tests/                   # unit + API tests
├── docs/design.md           # design document
└── pyproject.toml           # deps (uv)
```
