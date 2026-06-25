from backend.models import PILE_COUNT, ROW_SIZES, Card, GameState, Pile, Player


def make_card(pair_id: int) -> Card:
    return Card(pair_id=pair_id, name=f"C{pair_id}", color="#000", image="x.png", text="t")


def test_row_sizes_sum_to_pile_count():
    assert ROW_SIZES == (3, 5, 5, 3)
    assert PILE_COUNT == 16


def test_card_matches_by_pair_id_only():
    a = Card(1, "Fox", "#E86B3A", "fox.png", "Clever")
    b = Card(1, "Fox", "#E86B3A", "fox.png", "Clever")
    c = Card(2, "Whale", "#3A7BE8", "whale.png", "Deep")
    assert a.matches(b)
    assert not a.matches(c)


def test_card_is_frozen_and_hashable():
    assert make_card(1) == make_card(1)
    assert len({make_card(1), make_card(1)}) == 1


def test_pile_top_and_empty():
    pile = Pile()
    assert pile.is_empty
    assert pile.top is None
    pile.cards.extend([make_card(1), make_card(2)])
    assert not pile.is_empty
    assert pile.top.pair_id == 1


def test_pile_remove_top():
    pile = Pile([make_card(1), make_card(2)])
    removed = pile.remove_top()
    assert removed.pair_id == 1
    assert pile.top.pair_id == 2


def test_cycle_top_to_bottom_swaps_top():
    pile = Pile([make_card(1), make_card(2)])
    pile.cycle_top_to_bottom()
    assert [c.pair_id for c in pile.cards] == [2, 1]


def test_cycle_top_to_bottom_noop_on_single_card():
    pile = Pile([make_card(1)])
    pile.cycle_top_to_bottom()
    assert [c.pair_id for c in pile.cards] == [1]


def test_player_score_counts_pairs():
    p = Player("A")
    assert p.score == 0
    p.pairs.append(make_card(1))
    assert p.score == 1


def test_gamestate_helpers():
    state = GameState(piles=[Pile() for _ in range(16)], players=(Player("A"), Player("B")))
    assert state.current_player.name == "A"
    assert state.collected_pairs == 0
    state.players[0].pairs.append(make_card(1))
    assert state.collected_pairs == 1
