"""FastAPI app — the thin web boundary around the game core.

This layer holds *no* game rules. It receives player taps over HTTP, delegates
to :class:`backend.game.Game`, and serializes the result to JSON. Game instances
live in memory keyed by a game id.

Phase 1 (single-device pass-and-play) uses plain REST: there is no second client
to push updates to, so a WebSocket would add nothing. Phase 2 (online) would add
a WebSocket endpoint here that broadcasts state to both connected players —
without touching the core.

Serialization deliberately never exposes the faces of face-down cards. A card's
identity is returned only in the ``MoveResult`` of the tap that reveals it, so a
client cannot inspect the board it isn't allowed to see.
"""

from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.game import Game, InvalidMove, MoveResult
from backend.models import Card, GameState
from backend.themes.animals import ANIMAL_THEME

THEMES: dict[str, list[dict]] = {"animals": ANIMAL_THEME}

app = FastAPI(title="MemoryNinja", version="0.1.0")

# In-memory game store. Fine for Phase 1; a real deployment would use something
# with a lifecycle (eviction, persistence).
_games: dict[str, Game] = {}


# -- request / response models -----------------------------------------------


class NewGameRequest(BaseModel):
    player1: str = "Player 1"
    player2: str = "Player 2"
    theme: str = "animals"
    seed: int | None = Field(default=None, description="Set for a reproducible deal")


def _serialize_card(card: Card) -> dict:
    return {
        "pair_id": card.pair_id,
        "name": card.name,
        "color": card.color,
        "image": card.image,
        "text": card.text,
    }


def _serialize_state(state: GameState) -> dict:
    """Public view of the board — counts only, never face-down card faces."""
    return {
        "game_over": state.game_over,
        "current_player_index": state.current_player_index,
        "phase": "awaiting_second" if state.first_pick_index is not None else "awaiting_first",
        "first_pick_index": state.first_pick_index,
        "collected_pairs": state.collected_pairs,
        "players": [{"name": p.name, "score": p.score} for p in state.players],
        "piles": [
            {"index": i, "is_empty": pile.is_empty, "count": len(pile.cards)}
            for i, pile in enumerate(state.piles)
        ],
    }


def _serialize_move(result: MoveResult) -> dict:
    return {
        "pile_index": result.pile_index,
        "card": _serialize_card(result.card),  # the just-revealed face
        "phase": result.phase.value,
        "matched": result.matched,
        "turn_passed": result.turn_passed,
        "game_over": result.game_over,
        "winner": None if result.winner is None else {"name": result.winner.name},
    }


def _get_game(game_id: str) -> Game:
    game = _games.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail=f"no game with id {game_id!r}")
    return game


# -- endpoints ---------------------------------------------------------------


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "games": len(_games), "themes": list(THEMES)}


@app.post("/api/games", status_code=201)
def create_game(req: NewGameRequest) -> dict:
    if req.theme not in THEMES:
        raise HTTPException(status_code=400, detail=f"unknown theme {req.theme!r}")
    game = Game(
        player_names=(req.player1, req.player2),
        theme=THEMES[req.theme],
        seed=req.seed,
    )
    game_id = uuid.uuid4().hex
    _games[game_id] = game
    return {"game_id": game_id, "state": _serialize_state(game.state)}


@app.get("/api/games/{game_id}")
def get_game(game_id: str) -> dict:
    game = _get_game(game_id)
    return {"game_id": game_id, "state": _serialize_state(game.state)}


@app.post("/api/games/{game_id}/select/{pile_index}")
def select_pile(game_id: str, pile_index: int) -> dict:
    game = _get_game(game_id)
    try:
        result = game.select_pile(pile_index)
    except InvalidMove as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"move": _serialize_move(result), "state": _serialize_state(game.state)}


# Serve the frontend at the root once it exists. Mounted last so it never
# shadows the /api routes above.
_frontend = Path(__file__).resolve().parent.parent / "frontend"
if _frontend.is_dir():
    app.mount("/", StaticFiles(directory=str(_frontend), html=True), name="frontend")
