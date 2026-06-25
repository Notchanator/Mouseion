# MemoryNinja — Project Design Document

## Overview

MemoryNinja is a browser-based, mobile-friendly 1v1 memory card game. Players take turns flipping cards arranged in a 3-5-5-3 grid, trying to find matching pairs. The game supports swappable themes and is designed for single-device (pass-and-play) use first, with online multiplayer planned for a future phase.

---

## Game Rules

- **Cards:** 32 cards total (16 pairs), dealt 2 per pile across 16 piles
- **Grid layout:** 4 rows arranged in a 3-5-5-3 pattern (diamond/hourglass shape)
- **Turn flow:**
  1. Active player taps a pile — the top card flips face-up and **stays face-up**
  2. Player taps a second pile — that card flips face-up; **both cards stay face-up together for 3 seconds**, then the turn resolves
  3. **Match** → both cards are removed, the pile slot remains as an empty placeholder, player goes again
  4. **No match** → both cards flip face-down, each moves to the bottom of its respective pile, turn passes to the other player
- **Visual aid:** the two picks of a turn are nudged in opposite diagonal directions (first up-left, second down-right) so they read as distinct while both are face-up — a small extra hook for memory
- **Scoreboard timing:** the score and active-player indicator update when the cards visually resolve (after the 3-second hold), not at the instant the tap is registered
- **End condition:** all 16 pairs have been collected
- **Winner:** player with the most pairs; ties are allowed

---

## Card Design

Each card face consists of:
- **Background color** — unique per pair
- **Title / name** — displayed prominently (e.g. "Fox")
- **Central image** — artwork provided per theme (e.g. `fox.png`)
- **Flavor text** — a short descriptor at the bottom (e.g. "Clever & quick")

All face-down cards share a universal card back design (`card-back.png`).

---

## Project Structure

```
MemoryNinja/
│
├── backend/
│   ├── main.py                  # FastAPI app entry point, WebSocket endpoints
│   ├── game.py                  # Core game logic (state, turns, matching)
│   ├── models.py                # Data classes (Card, Pile, GameState, Player)
│   └── themes/
│       ├── __init__.py
│       └── animals.py           # Animal theme card definitions
│
├── frontend/
│   ├── index.html               # App shell, loads everything
│   ├── style.css                # Layout, card styling, animations
│   ├── app.js                   # Entry point, initializes the game
│   ├── board.js                 # Renders the 3-5-5-3 grid, manages piles
│   ├── card.js                  # Card component, flip animation logic
│   ├── gameState.js             # Mirrors server state on the client
│   └── assets/
│       ├── card-back.png        # Universal card back design
│       └── themes/
│           └── animals/
│               ├── fox.png
│               ├── whale.png
│               └── ...          # One image per animal (16 total)
│
├── docs/
│   └── design.md                # This document
│
├── tests/
│   ├── test_game.py             # Unit tests for game logic
│   └── test_models.py           # Unit tests for data models
│
├── requirements.txt             # Python dependencies (FastAPI, uvicorn, etc.)
└── README.md                    # Setup and run instructions
```

---

## Component Responsibilities

### Backend

| File | Responsibility |
|------|----------------|
| `main.py` | Thin web layer — receives player actions via WebSocket, delegates to `game.py` |
| `game.py` | Pure game logic — no web, no UI. Handles shuffling, turn management, matching, win detection. Fully unit-testable in isolation. |
| `models.py` | Data shapes used across the backend — `Card`, `Pile`, `GameState`, `Player` |
| `themes/animals.py` | Animal theme card definitions (name, color, image path, flavor text) |

### Frontend

| File | Responsibility |
|------|----------------|
| `index.html` | App shell — loads CSS, JS, provides root DOM element |
| `style.css` | All visual styling — layout, card faces, flip animations, mobile responsiveness |
| `app.js` | Entry point — initializes the board, connects to backend, wires up events |
| `board.js` | Renders the 3-5-5-3 grid; manages pile slots including empty placeholders |
| `card.js` | Individual card rendering and 3D flip animation logic |
| `gameState.js` | Keeps frontend in sync with server state; no game logic lives here |

---

## Theme Architecture

Themes are designed to be fully swappable by touching only two locations:

- **Backend:** add a new file at `backend/themes/<themename>.py`
- **Frontend:** add a new folder at `frontend/assets/themes/<themename>/`

### Card Data Structure

```python
ANIMAL_THEME = [
    { "id": 1,  "name": "Fox",   "color": "#E86B3A", "image": "fox.png",   "text": "Clever & quick" },
    { "id": 2,  "name": "Whale", "color": "#3A7BE8", "image": "whale.png", "text": "Deep & wise" },
    # ... 16 total entries
]
```

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend language | Python |
| Web framework | FastAPI |
| Real-time communication | WebSockets (FastAPI native) |
| Frontend | HTML + CSS + Vanilla JavaScript |
| Deployment (planned) | Railway / Render / Fly.io |

---

## Development Phases

### Phase 1 — Single Device (Current)
- Full game logic in Python
- Pass-and-play on one device/browser
- Animal theme with placeholder assets

### Phase 2 — Online Multiplayer (Planned)
- Two players connect via shared game URL
- Real-time sync via WebSocket
- Player name entry, lobby/waiting state

### Phase 3 — Polish (Planned)
- Custom artwork integrated
- Additional themes
- Sound effects and card flip audio
- Score history / win tracking
