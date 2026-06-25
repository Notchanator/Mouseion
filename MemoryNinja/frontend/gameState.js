// Mirrors the server's game state on the client. Holds NO game logic — it only
// talks to the /api endpoints and caches the latest state the server returned.

const API = "/api";

export class GameState {
  constructor() {
    this.gameId = null;
    this.state = null; // latest public board state from the server
  }

  get phase() {
    return this.state ? this.state.phase : "awaiting_first";
  }
  get firstPickIndex() {
    return this.state ? this.state.first_pick_index : null;
  }
  get isOver() {
    return this.state ? this.state.game_over : false;
  }
  pile(i) {
    return this.state.piles[i];
  }

  async newGame({ player1, player2, theme = "animals", seed = null } = {}) {
    const body = { player1, player2, theme };
    if (seed !== null) body.seed = seed;
    const res = await fetch(`${API}/games`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(await detail(res));
    const data = await res.json();
    this.gameId = data.game_id;
    this.state = data.state;
    return this.state;
  }

  // Returns the `move` describing what the tap revealed/resolved, and updates
  // the cached state. Throws on an illegal tap (HTTP 400).
  async select(pileIndex) {
    const res = await fetch(`${API}/games/${this.gameId}/select/${pileIndex}`, {
      method: "POST",
    });
    if (!res.ok) throw new Error(await detail(res));
    const data = await res.json();
    this.state = data.state;
    return data.move;
  }
}

async function detail(res) {
  try {
    return (await res.json()).detail || res.statusText;
  } catch {
    return res.statusText;
  }
}
