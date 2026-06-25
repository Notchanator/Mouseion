"""Data shapes used across the MemoryNinja backend.

These types hold state only. All game *logic* (shuffling, turn flow, matching,
win detection) lives in ``game.py`` so that this module stays a pure description
of the data and can be reused regardless of how the game is served.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# The board is 16 piles laid out in a 3-5-5-3 (diamond/hourglass) grid.
# The core keeps piles as a flat list; the frontend maps indices onto rows.
ROW_SIZES: tuple[int, ...] = (3, 5, 5, 3)
PILE_COUNT: int = sum(ROW_SIZES)  # 16


@dataclass(frozen=True)
class Card:
    """A single card face.

    Two cards form a matching pair when they share the same ``pair_id``. The
    remaining fields are presentation data supplied by a theme.
    """

    pair_id: int
    name: str
    color: str
    image: str
    text: str

    def matches(self, other: "Card") -> bool:
        return self.pair_id == other.pair_id


@dataclass
class Pile:
    """A stack of cards at one board slot.

    The card at index 0 is the *top* (the one revealed when the pile is tapped);
    the card at the end is the *bottom*. A pile with no cards is an empty
    placeholder slot.
    """

    cards: list[Card] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.cards

    @property
    def top(self) -> Card | None:
        return self.cards[0] if self.cards else None

    def remove_top(self) -> Card:
        """Remove and return the top card (used when a pair is collected)."""
        return self.cards.pop(0)

    def cycle_top_to_bottom(self) -> None:
        """Move the top card to the bottom (used on a failed match)."""
        if len(self.cards) > 1:
            self.cards.append(self.cards.pop(0))


@dataclass
class Player:
    """A player and the pairs they have collected."""

    name: str
    # One representative card per collected pair.
    pairs: list[Card] = field(default_factory=list)

    @property
    def score(self) -> int:
        return len(self.pairs)


@dataclass
class GameState:
    """The full state of a game in progress."""

    piles: list[Pile]
    players: tuple[Player, Player]
    current_player_index: int = 0
    # The pile index revealed by the first tap of the current turn, if any.
    first_pick_index: int | None = None
    game_over: bool = False

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    @property
    def collected_pairs(self) -> int:
        return sum(p.score for p in self.players)
