import random
from collections import Counter

import pytest

from backend.game import Game, InvalidMove, Phase, deal
from backend.models import PILE_COUNT, Card, Pile
from backend.themes.animals import ANIMAL_THEME


def card(pair_id: int) -> Card:
    return Card(pair_id=pair_id, name=f"C{pair_id}", color="#000", image="x.png", text="t")


# -- deal --------------------------------------------------------------------


def test_deal_produces_16_piles_of_two():
    piles = deal(ANIMAL_THEME, random.Random(0))
    assert len(piles) == PILE_COUNT
    assert all(len(p.cards) == 2 for p in piles)


def test_deal_uses_every_card_exactly_twice():
    piles = deal(ANIMAL_THEME, random.Random(7))
    counts = Counter(c.pair_id for p in piles for c in p.cards)
    assert set(counts) == {e["id"] for e in ANIMAL_THEME}
    assert all(n == 2 for n in counts.values())


def test_deal_splits_every_pair_across_distinct_piles():
    # The key invariant that keeps the game winnable: no pile holds both copies
    # of a pair.
    for seed in range(50):
        piles = deal(ANIMAL_THEME, random.Random(seed))
        for pile in piles:
            assert pile.cards[0].pair_id != pile.cards[1].pair_id


def test_deal_is_deterministic_for_a_seed():
    a = deal(ANIMAL_THEME, random.Random(42))
    b = deal(ANIMAL_THEME, random.Random(42))
    assert [[c.pair_id for c in p.cards] for p in a] == [
        [c.pair_id for c in p.cards] for p in b
    ]


def test_deal_rejects_wrong_sized_theme():
    with pytest.raises(ValueError):
        deal(ANIMAL_THEME[:10], random.Random(0))


# -- turn flow ---------------------------------------------------------------


def new_game() -> Game:
    return Game(seed=0)


def test_first_pick_reveals_and_awaits_second():
    game = new_game()
    result = game.select_pile(0)
    assert game.phase is Phase.AWAITING_SECOND
    assert result.card is game.state.piles[0].cards[0]
    assert result.matched is None


def test_match_collects_pair_and_player_goes_again():
    game = new_game()
    game.state.piles[0] = Pile([card(1), card(9)])
    game.state.piles[1] = Pile([card(1), card(9)])

    game.select_pile(0)
    result = game.select_pile(1)

    assert result.matched is True
    assert result.turn_passed is False
    assert game.phase is Phase.AWAITING_FIRST
    assert game.state.current_player_index == 0  # same player
    assert game.state.players[0].score == 1
    # Tops removed; the bottoms remain.
    assert [c.pair_id for c in game.state.piles[0].cards] == [9]
    assert [c.pair_id for c in game.state.piles[1].cards] == [9]


def test_miss_cycles_both_piles_and_passes_turn():
    game = new_game()
    game.state.piles[0] = Pile([card(1), card(2)])
    game.state.piles[1] = Pile([card(3), card(4)])

    game.select_pile(0)
    result = game.select_pile(1)

    assert result.matched is False
    assert result.turn_passed is True
    assert game.state.current_player_index == 1  # turn passed
    assert [c.pair_id for c in game.state.piles[0].cards] == [2, 1]
    assert [c.pair_id for c in game.state.piles[1].cards] == [4, 3]
    assert game.state.players[0].score == 0


# -- invalid moves -----------------------------------------------------------


def test_second_pile_must_differ_from_first():
    game = new_game()
    game.select_pile(0)
    with pytest.raises(InvalidMove):
        game.select_pile(0)


def test_cannot_select_empty_pile():
    game = new_game()
    game.state.piles[5] = Pile([])
    with pytest.raises(InvalidMove):
        game.select_pile(5)


def test_cannot_select_out_of_range():
    game = new_game()
    with pytest.raises(InvalidMove):
        game.select_pile(99)


def test_cannot_move_after_game_over():
    game = new_game()
    game.state.game_over = True
    with pytest.raises(InvalidMove):
        game.select_pile(0)


# -- end conditions ----------------------------------------------------------


def _stack_board(game: Game) -> None:
    """8 pile-pairs, each yielding two matchable pairs (tops then bottoms)."""
    for j in range(8):
        game.state.piles[2 * j] = Pile([card(j), card(j + 8)])
        game.state.piles[2 * j + 1] = Pile([card(j), card(j + 8)])


def test_full_game_declares_winner():
    game = Game(player_names=("Ann", "Bo"), seed=0)
    _stack_board(game)

    result = None
    for j in range(8):
        game.select_pile(2 * j)        # match top pair j
        game.select_pile(2 * j + 1)
        game.select_pile(2 * j)        # match new top pair j+8
        result = game.select_pile(2 * j + 1)

    assert result.game_over is True
    assert game.state.game_over is True
    # Player 0 never missed, so collected all 16 pairs.
    assert result.winner is game.state.players[0]
    assert game.state.players[0].score == 16


def test_tie_reports_no_winner():
    game = Game(player_names=("Ann", "Bo"), seed=0)
    # Pre-load 15 collected pairs split 7 (P0) / 8 (P1), leaving one on the board.
    for i in range(7):
        game.state.players[0].pairs.append(card(100 + i))
    for i in range(8):
        game.state.players[1].pairs.append(card(200 + i))
    game.state.piles = [Pile([]) for _ in range(PILE_COUNT)]
    game.state.piles[0] = Pile([card(1)])
    game.state.piles[1] = Pile([card(1)])
    game.state.current_player_index = 0  # P0 takes the last pair -> 8-8

    game.select_pile(0)
    result = game.select_pile(1)

    assert result.game_over is True
    assert result.winner is None  # tie
    assert game.state.players[0].score == game.state.players[1].score == 8
