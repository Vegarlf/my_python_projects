"""Test Deck"""

import pytest

# from ..src import card_engine as cg
import card_engine as cg
from colorama import Fore
from random import randint, choice, seed  # pyright: ignore[reportUnusedImport]
from conftest import FLAKYRERUN

pytestmark = pytest.mark.test_deck


def test_deck_init(
    setup: tuple[cg.Deck, list[cg.Card]], capsys: pytest.CaptureFixture[str]
) -> None:
    """Test Deck Class Initialisation"""
    d, pre = setup  # pyright: ignore[reportUnusedVariable]
    assert hasattr(d, "id")
    assert hasattr(d, "deck")
    assert d.id == "def"
    assert len(d.deck) == 52
    assert len(set(d.deck)) == len(d.deck)
    assert cg.Deck.instance_count == 1
    assert len(cg.Deck.INSTANCE_LIST) == 1
    assert cg.Deck.INSTANCE_LIST[0] == d
    d2 = cg.Deck()
    noshow = capsys.readouterr()  # pyright: ignore[reportUnusedVariable]
    assert cg.Deck.instance_count == 1
    assert len(cg.Deck.INSTANCE_LIST) == 1
    assert not hasattr(d2, "deck")
    assert not hasattr(d2, "id")
    assert d.deck[0] == cg.Card("2", "H")
    assert d.deck[-1] == cg.Card("A", "C")


def test_deck_print(setup: tuple[cg.Deck, list[cg.Card]]) -> None:
    """Test Deck Print"""
    d, pre = setup  # pyright: ignore[reportUnusedVariable]
    assert all(color in str(d) for color in [Fore.RED, Fore.BLUE])
    assert ", " in str(d)
    assert len(str(d).split(", ")) == 52


def test_deck_shuffle(setup: tuple[cg.Deck, list[cg.Card]]) -> None:
    """Test Deck Shuffle Function"""
    step = randint(1, 99)
    d, pre = setup
    d.shuffle(step)
    assert d.deck != pre
    assert len(d.deck) == len(pre)


@pytest.mark.flaky(reruns=FLAKYRERUN, only_rerun=["HEYNOAH"])
def test_deck_take_cards(
    setup: tuple[cg.Deck, list[cg.Card]], capsys: pytest.CaptureFixture[str]
) -> None:
    """Test Deck Take Card Function"""
    d, pre = setup
    count: int = randint(1, (len(d.deck) - 1))
    rdtake: bool = choice([True, False])
    shuffleafter: bool = choice([True, False])
    taken: list[cg.Card] = d.take_cards(count, rdtake, shuffleafter)
    assert len(set(taken)) == len(taken)
    assert taken
    for x in taken:
        assert isinstance(x, cg.Card)
    assert len(taken) < len(pre)
    assert len([c for c in taken if c in pre]) == len(taken)
    assert set(taken).isdisjoint(set(d.deck))
    assert len(d.deck) == (len(pre) - len(taken))
    if rdtake:
        assert taken != pre[::-1][:count]
    else:
        assert taken == pre[::-1][:count]
    if shuffleafter:
        assert d.deck != [x for x in pre if x not in taken], "HEYNOAH"
    else:
        assert d.deck == [x for x in pre if x not in taken]
    cg.reset_game()
    dc: cg.Deck = cg.Deck()
    prc: list[cg.Card] = dc.deck.copy()
    assert not dc.take_cards((len(dc.deck) + 1))
    noshow = capsys.readouterr()  # pyright: ignore[reportUnusedVariable]
    assert dc.deck == prc


def test_deck_put_cards(
    setup: tuple[cg.Deck, list[cg.Card]], capsys: pytest.CaptureFixture[str]
) -> None:
    """Test Deck Put Card Function."""
    d, pre = setup
    to_put: list[cg.Card] = d.take_cards(randint(1, len(d.deck) - 1), True, True)
    assert to_put
    assert len(to_put) < len(pre)
    assert not set(to_put).issubset(set(d.deck))
    shuffleafter: bool = choice([True, False])
    deck_bf_len = len(d.deck)
    to_put_len: int = len(to_put)
    d.put_cards(to_put, shuffleafter)
    assert set(to_put).issubset(set(d.deck))
    assert len(d.deck) == deck_bf_len + to_put_len
    to_put_copy: list[cg.Card] = to_put.copy()
    deck_bf_len2: int = len(d.deck)
    invalid_added: int = randint(1, len(d.deck) - 1)
    for _ in range(invalid_added):
        to_put.append(d.deck[randint(0, len(d.deck) - 1)])
    assert (set(to_put) - set(to_put_copy)).issubset(set(d.deck))
    to_put_len2: int = len(to_put)
    d.put_cards(to_put, shuffleafter)
    noshow = capsys.readouterr()  # pyright: ignore[reportUnusedVariable]
    assert to_put_len2 == len(to_put)
    assert deck_bf_len2 == len(d.deck)
    assert set(to_put).issubset(set(d.deck))


def test_deck_search_card_loc_deck(setup: tuple[cg.Deck, list[cg.Card]]) -> None:
    """Test Deck Search Hand Function."""
    d, pre = setup  # pyright: ignore[reportUnusedVariable]
    assert True
    index1: int = randint(0, ((len(d.deck) // 2) - 1))
    index2: int = randint((len(d.deck) // 2), len(d.deck) - 1)
    taken: list[cg.Card] = d.deck[index1:index2]
    assert taken
    assert len(taken) <= len(d.deck)
    assert set(taken).issubset(set(d.deck))
    no_find: list[cg.Card] = d.take_cards(randint(1, (len(d.deck) // 2) - 1), True, True)
    expected_find: int = len(set(taken) & set(d.deck))
    taken.extend(no_find)
    loc_dict: dict[cg.Card, int | None] = d.search_card_loc_deck(taken)
    nonecount: int = 0
    foundcount: int = 0
    for k, v in loc_dict.items():
        assert isinstance(k, cg.Card)
        assert isinstance(v, int | None)
        if isinstance(v, int):
            assert k == d.deck[v]
            foundcount += 1
        elif v is None:
            assert k not in d.deck
            nonecount += 1
    assert nonecount == len(no_find)
    assert foundcount == expected_find


@pytest.mark.testreset
def test_xx() -> None:
    assert not cg.Deck.instance_count, "setup deck teardown failure"
    assert not cg.Deck.INSTANCE_LIST, "setup deck teardown failure"
