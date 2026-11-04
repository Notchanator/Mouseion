import pytest
from fastapi.testclient import TestClient

from backend import main
from backend.main import app


@pytest.fixture
def client():
    main._games.clear()
    return TestClient(app)


def create(client, **body):
    body.setdefault("seed", 0)
    resp = client.post("/api/games", json=body)
    assert resp.status_code == 201
    return resp.json()


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert "animals" in resp.json()["themes"]


def test_create_game_returns_id_and_initial_state(client):
    data = create(client, player1="Ann", player2="Bo")
    assert "game_id" in data
    state = data["state"]
    assert state["game_over"] is False
    assert state["phase"] == "awaiting_first"
    assert [p["name"] for p in state["players"]] == ["Ann", "Bo"]
    assert len(state["piles"]) == 16
    assert all(p["count"] == 2 and not p["is_empty"] for p in state["piles"])


def test_state_never_leaks_facedown_card_faces(client):
    # The public board view must expose counts only — no pair_id/name/etc.
    data = create(client)
    pile = data["state"]["piles"][0]
    assert set(pile) == {"index", "is_empty", "count"}


def test_unknown_theme_rejected(client):
    resp = client.post("/api/games", json={"theme": "dinosaurs"})
    assert resp.status_code == 400


def test_get_missing_game_is_404(client):
    assert client.get("/api/games/nope").status_code == 404


def test_select_reveals_card_then_resolves(client):
    game_id = create(client)["game_id"]
    # Force a known match on the server-side game object.
    from backend.models import Card, Pile

    def card(pid):
        return Card(pid, f"C{pid}", "#000", "x.png", "t")

    g = main._games[game_id]
    g.state.piles[0] = Pile([card(1), card(9)])
    g.state.piles[1] = Pile([card(1), card(9)])

    first = client.post(f"/api/games/{game_id}/select/0").json()
    assert first["move"]["card"]["pair_id"] == 1  # reveal returns the face
    assert first["move"]["matched"] is None
    assert first["state"]["phase"] == "awaiting_second"

    second = client.post(f"/api/games/{game_id}/select/1").json()
    assert second["move"]["matched"] is True
    assert second["state"]["players"][0]["score"] == 1
    assert second["state"]["phase"] == "awaiting_first"


def test_invalid_move_is_400(client):
    game_id = create(client)["game_id"]
    client.post(f"/api/games/{game_id}/select/0")
    resp = client.post(f"/api/games/{game_id}/select/0")  # same pile twice
    assert resp.status_code == 400


def test_select_on_missing_game_is_404(client):
    assert client.post("/api/games/nope/select/0").status_code == 404
