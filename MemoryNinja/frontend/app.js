// Entry point. Wires the board to the server, and owns the *timing* of a turn:
// reveal a tapped card for a few seconds, then hide it; on the second tap,
// resolve match (collect both) or miss (hide both, turn passes). All rules live
// on the server — this file only sequences animations around its responses.

import { renderBoard, applyState } from "./board.js";
import { setFace, flipUp, flipDown, markMatched, clearMatched } from "./card.js";
import { GameState } from "./gameState.js";

const REVEAL_MS = 3000; // design.md: each flipped card shows for 3 seconds
const FLIP_MS = 500; // matches --flip-ms in style.css

const game = new GameState();
let piles = []; // pile views from board.js, indexed by pile index
let busy = false; // locks input during a reveal/resolve animation
let firstIndex = null; // pile chosen by the first tap of the current turn

const els = {
  board: document.getElementById("board"),
  hint: document.getElementById("turn-hint"),
  scores: [document.getElementById("score-0"), document.getElementById("score-1")],
  players: [...document.querySelectorAll(".player")],
  names: [...document.querySelectorAll(".player-name")],
  newGame: document.getElementById("new-game"),
  overlay: document.getElementById("overlay"),
  overlayTitle: document.getElementById("overlay-title"),
  overlayDetail: document.getElementById("overlay-detail"),
  overlayNew: document.getElementById("overlay-new"),
};

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function startGame() {
  hideOverlay();
  busy = true;
  firstIndex = null;
  // Optional ?seed=N gives a reproducible deal (handy for replays / testing).
  const seedParam = new URLSearchParams(location.search).get("seed");
  await game.newGame({
    player1: els.names[0].value.trim() || "Player 1",
    player2: els.names[1].value.trim() || "Player 2",
    seed: seedParam !== null ? Number(seedParam) : null,
  });
  piles = renderBoard(els.board, onPileClick);
  applyState(piles, game.state);
  busy = false;
  updateHud();
}

async function onPileClick(index) {
  if (busy || game.isOver || !game.state) return;
  if (game.pile(index).is_empty) return;

  if (game.phase === "awaiting_first") {
    await revealFirst(index);
  } else if (index !== game.firstPickIndex) {
    await revealSecond(index);
  }
}

async function revealFirst(index) {
  busy = true;
  firstIndex = index;
  const move = await game.select(index);
  const { cardEl } = piles[index];
  setFace(cardEl, move.card);
  cardEl.classList.add("pick-first"); // nudged up-left for distinction
  flipUp(cardEl);
  updateHud();
  // The first card stays face-up until the second card's reveal ends — just let
  // the flip finish, then unlock so the player can pick the second pile.
  await wait(FLIP_MS);
  busy = false;
}

async function revealSecond(index) {
  busy = true;
  const move = await game.select(index);
  const cardEl = piles[index].cardEl;
  const firstCardEl = piles[firstIndex].cardEl;
  setFace(cardEl, move.card);
  cardEl.classList.add("pick-second"); // nudged down-right for distinction
  flipUp(cardEl);
  // Note: do NOT refresh the HUD here. The server has already applied the
  // outcome (score, turn change), but visually the cards are still face-up for
  // the reveal — so we leave the scoreboard showing the current player until the
  // cards resolve, then update once below.

  // Both cards are face-up now (the first has stayed up); hold them together.
  await wait(REVEAL_MS);

  if (move.matched) {
    markMatched(cardEl);
    markMatched(firstCardEl);
    await wait(600);
  }
  // Flip both back down and clear their offsets/highlights.
  [cardEl, firstCardEl].forEach((el) => {
    clearMatched(el);
    flipDown(el);
    el.classList.remove("pick-first", "pick-second");
  });
  await wait(FLIP_MS);

  applyState(piles, game.state); // reflect removals / emptied piles
  firstIndex = null;
  busy = false;
  updateHud();

  if (move.game_over) showOverlay(move.winner);
}

function updateHud() {
  const s = game.state;
  if (!s) return;
  s.players.forEach((p, i) => {
    els.scores[i].textContent = p.score;
    els.players[i].classList.toggle("active", i === s.current_player_index && !s.game_over);
  });
  if (s.game_over) {
    els.hint.textContent = "Game over";
  } else if (s.phase === "awaiting_second") {
    els.hint.textContent = "Tap a second pile to match";
  } else {
    els.hint.textContent = `${s.players[s.current_player_index].name}, tap a pile`;
  }
}

function showOverlay(winner) {
  els.overlayTitle.textContent = winner ? `${winner.name} wins!` : "It's a tie!";
  const [a, b] = game.state.players;
  els.overlayDetail.textContent = `Final score — ${a.name}: ${a.score}, ${b.name}: ${b.score}`;
  els.overlay.classList.remove("hidden");
}
function hideOverlay() {
  els.overlay.classList.add("hidden");
}

els.newGame.addEventListener("click", startGame);
els.overlayNew.addEventListener("click", startGame);
