"""Core MemoryNinja game logic.

Pure logic only — no web layer, no UI, no timers. The 3-second card-flip is a
presentation concern handled by the frontend; this module just resolves what a
tap *means*. Everything here is deterministic given a seeded ``random.Random``,
which keeps it fully unit-testable in isolation.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

from backend.models import PILE_COUNT, Card, GameState, Pile, Player


class InvalidMove(Exception):
    """Raised when a tap is not legal in the current game state."""


class Phase(Enum):
    """Which tap of the current turn we are waiting for."""

    AWAITING_FIRST = "awaiting_first"
    AWAITING_SECOND = "awaiting_second"


@dataclass
class MoveResult:
    """Describes the outcome of a single ``select_pile`` call.

    The frontend uses this to drive animations: reveal ``card`` (flip face-up
    for 3s), and on the second tap react to ``matched``.
    """

    pile_index: int
    card: Card
    phase: Phase  # the phase *after* this move resolves
    # Populated only on the second tap of a turn:
    matched: bool | None = None
    turn_passed: bool = False
    game_over: bool = False
    # On game over: the winning Player, or None for a tie.
    winner: Player | None = None


def _build_cards(theme: list[dict]) -> tuple[list[Card], list[Card]]:
    """Return two parallel lists holding the first and second copy of each pair."""
    firsts, seconds = [], []
    for entry in theme:
        card = Card(
            pair_id=entry["id"],
            name=entry["name"],
            color=entry["color"],
            image=entry["image"],
            text=entry["text"],
        )
        firsts.append(card)
        seconds.append(card)
    return firsts, seconds


def deal(theme: list[dict], rng: random.Random) -> list[Pile]:
    """Deal a theme into 16 piles of 2 cards.

    Guarantees the two cards of every pair land in *different* piles. Cards never
    move between piles during play, so a pair whose copies share a pile could
    never be collected — splitting them keeps the "all 16 pairs collected" end
    state reachable.
    """
    if len(theme) != PILE_COUNT:
        raise ValueError(f"theme must define exactly {PILE_COUNT} pairs, got {len(theme)}")

    firsts, seconds = _build_cards(theme)
    order = list(range(PILE_COUNT))
    rng.shuffle(order)
    firsts = [firsts[i] for i in order]
    seconds = [seconds[i] for i in order]
    # Rotate the second copies by one: a fixed-point-free mapping that guarantees
    # pile i never receives both copies of the same pair.
    seconds = seconds[1:] + seconds[:1]

    piles: list[Pile] = []
    for first, second in zip(firsts, seconds):
        two = [first, second]
        rng.shuffle(two)  # randomize which copy starts on top
        piles.append(Pile(cards=two))
    return piles


class Game:
    """Orchestrates a single MemoryNinja match over a :class:`GameState`."""

    def __init__(
        self,
        player_names: tuple[str, str] = ("Player 1", "Player 2"),
        theme: list[dict] | None = None,
        seed: int | None = None,
    ) -> None:
        if theme is None:
            from backend.themes.animals import ANIMAL_THEME

            theme = ANIMAL_THEME
        rng = random.Random(seed)
        self.state = GameState(
            piles=deal(theme, rng),
            players=(Player(player_names[0]), Player(player_names[1])),
        )

    # -- queries -----------------------------------------------------------

    @property
    def phase(self) -> Phase:
        if self.state.first_pick_index is None:
            return Phase.AWAITING_FIRST
        return Phase.AWAITING_SECOND

    def _winner(self) -> Player | None:
        a, b = self.state.players
        if a.score == b.score:
            return None
        return a if a.score > b.score else b

    # -- the single action -------------------------------------------------

    def select_pile(self, index: int) -> MoveResult:
        """Tap a pile. The first tap of a turn reveals; the second resolves it."""
        if self.state.game_over:
            raise InvalidMove("the game is over")
        if not 0 <= index < len(self.state.piles):
            raise InvalidMove(f"pile index {index} out of range")
        pile = self.state.piles[index]
        if pile.is_empty:
            raise InvalidMove(f"pile {index} is empty")

        if self.phase is Phase.AWAITING_FIRST:
            return self._first_pick(index, pile)
        return self._second_pick(index, pile)

    # -- internals ---------------------------------------------------------

    def _first_pick(self, index: int, pile: Pile) -> MoveResult:
        self.state.first_pick_index = index
        return MoveResult(
            pile_index=index,
            card=pile.top,  # type: ignore[arg-type]  # non-empty checked above
            phase=Phase.AWAITING_SECOND,
        )

    def _second_pick(self, index: int, pile: Pile) -> MoveResult:
        first_index = self.state.first_pick_index
        assert first_index is not None
        if index == first_index:
            raise InvalidMove("second pile must differ from the first")

        first_pile = self.state.piles[first_index]
        first_card = first_pile.top
        second_card = pile.top
        assert first_card is not None and second_card is not None

        self.state.first_pick_index = None  # turn's reveal phase is done

        if first_card.matches(second_card):
            return self._resolve_match(index, second_card, first_pile, pile)
        return self._resolve_miss(index, second_card, first_pile, pile)

    def _resolve_match(
        self,
        index: int,
        second_card: Card,
        first_pile: Pile,
        pile: Pile,
    ) -> MoveResult:
        won = first_pile.remove_top()
        pile.remove_top()
        self.state.current_player.pairs.append(won)

        if self.state.collected_pairs == PILE_COUNT:
            self.state.game_over = True
            return MoveResult(
                pile_index=index,
                card=second_card,
                phase=Phase.AWAITING_FIRST,
                matched=True,
                game_over=True,
                winner=self._winner(),
            )

        # Matched player goes again.
        return MoveResult(
            pile_index=index,
            card=second_card,
            phase=Phase.AWAITING_FIRST,
            matched=True,
        )

    def _resolve_miss(
        self,
        index: int,
        second_card: Card,
        first_pile: Pile,
        pile: Pile,
    ) -> MoveResult:
        # Each revealed card drops to the bottom of its own pile, then the turn
        # passes to the other player.
        first_pile.cycle_top_to_bottom()
        pile.cycle_top_to_bottom()
        self.state.current_player_index ^= 1
        return MoveResult(
            pile_index=index,
            card=second_card,
            phase=Phase.AWAITING_FIRST,
            matched=False,
            turn_passed=True,
        )
