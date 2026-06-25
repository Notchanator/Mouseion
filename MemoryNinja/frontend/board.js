// Renders the 16 piles in the 3-5-5-3 (diamond) layout and keeps each pile's
// empty/occupied appearance in sync with server state. No game logic here.

import { createCard } from "./card.js";

const ROW_SIZES = [3, 5, 5, 3];

// Builds the board into `container` and returns an array of pile views indexed
// by pile index: { slot, cardEl }. `onPileClick(index)` fires on a tap.
export function renderBoard(container, onPileClick) {
  container.innerHTML = "";
  const piles = [];
  let index = 0;

  for (const size of ROW_SIZES) {
    const row = document.createElement("div");
    row.className = "board-row";

    for (let i = 0; i < size; i++) {
      const pileIndex = index++;
      const slot = document.createElement("div");
      slot.className = "pile";
      const cardEl = createCard();
      slot.appendChild(cardEl);
      slot.addEventListener("click", () => onPileClick(pileIndex));
      row.appendChild(slot);
      piles.push({ slot, cardEl });
    }
    container.appendChild(row);
  }
  return piles;
}

// Reflect pile counts: a pile with no cards shows the empty placeholder.
export function applyState(piles, state) {
  state.piles.forEach((p, i) => {
    piles[i].slot.classList.toggle("empty", p.is_empty);
  });
}
