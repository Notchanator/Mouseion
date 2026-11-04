// A single card's DOM and its flip animation. The board renders one card per
// pile slot — the top card. Revealing sets the face, then flips; hiding flips
// back. Art is a placeholder emoji so the game is playable without real assets;
// drop PNGs into assets/themes/<theme>/ and swap `renderArt` to use them.

const EMOJI = {
  Fox: "🦊", Whale: "🐋", Owl: "🦉", Rabbit: "🐰",
  Bear: "🐻", Frog: "🐸", Deer: "🦌", Otter: "🦦",
  Hedgehog: "🦔", Wolf: "🐺", Penguin: "🐧", Tiger: "🐯",
  Koala: "🐨", Hawk: "🦅", Seal: "🦭", Lynx: "🐈",
};

function renderArt(card) {
  return EMOJI[card.name] || card.name[0];
}

export function createCard() {
  const el = document.createElement("div");
  el.className = "card";
  el.innerHTML = `
    <div class="card-inner">
      <div class="card-face card-back"></div>
      <div class="card-face card-front"></div>
    </div>`;
  return el;
}

export function setFace(cardEl, card) {
  const front = cardEl.querySelector(".card-front");
  front.style.background = card.color;
  front.innerHTML = `
    <div class="card-name">${escapeHtml(card.name)}</div>
    <div class="card-art">${renderArt(card)}</div>
    <div class="card-text">${escapeHtml(card.text)}</div>`;
}

export function flipUp(cardEl) {
  cardEl.classList.add("flipped");
}
export function flipDown(cardEl) {
  cardEl.classList.remove("flipped");
}
export function markMatched(cardEl) {
  cardEl.classList.add("matched");
}
export function clearMatched(cardEl) {
  cardEl.classList.remove("matched");
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );
}
