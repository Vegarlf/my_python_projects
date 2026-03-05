"""Test Hand"""

from _pytest.capture import CaptureResult
import pytest

import card_engine as cg
from random import randint, choice
from conftest import RUNCOUNT, FLAKYRERUN
from collections import Counter
from collections.abc import Generator

pytestmark: pytest.MarkDecorator = pytest.mark.test_hand


@pytest.fixture(params=[n for n in range(RUNCOUNT)])
def setup() -> Generator[cg.Hand, None, None]:
    """
    Setup
    """
    cg.reset_game()
    h1: cg.Hand = cg.Hand(1)
    assert not h1.hand_c
    yield h1
    cg.reset_game()


def rand_cards(
    hand_to: cg.Hand, count_add: int = 0
) -> tuple[cg.Hand, list[cg.Card], int]:
    """Add Random Cards To Hand.
    ===========================

    Args:
    ====
        1) hand_to (): Hand Object - hand to add cards to\n
        2) count_add (): int - amount of random cards to add. Defaults to 0. If 0, Random Amount Of Cards Added.

    Returns:
    =======
    1)New Hand Object With Cards In Deck Attribute\n
    2)List Of Cards Added\n
    3)Amount Of Cards Added
    """
    card_count: int
    to_add_1: list[cg.Card]
    if not count_add:
        card_count = randint(1, 51)
        to_add_1 = []
        for _ in range(card_count):
            to_add_1.append(cg.Card(choice(cg.Card.RANKS), choice(cg.Card.SUITS)))
        assert len(to_add_1) == card_count
        assert to_add_1
        hand_to.hand_c.extend(to_add_1)
    else:
        card_count = count_add
        to_add_1 = []
        for _ in range(card_count):
            to_add_1.append(cg.Card(choice(cg.Card.RANKS), choice(cg.Card.SUITS)))
        assert len(to_add_1) == card_count
        assert to_add_1
        hand_to.hand_c.extend(to_add_1)
    return hand_to, to_add_1, card_count


def test_hand_init(setup: cg.Hand, capsys: pytest.CaptureFixture[str]) -> None:
    h1: cg.Hand = setup
    assert hasattr(h1, "hand_c")
    assert hasattr(h1, "id_hand")
    assert hasattr(h1, "type_hand")
    assert hasattr(h1, "is_hidden")
    assert not h1.hand_c
    assert h1.id_hand == 1
    assert h1.type_hand == "player"
    assert h1.is_hidden == False
    assert cg.Hand.instance_count == 1
    assert len(cg.Hand.INSTANCE_LIST) == 1
    h2: cg.Hand = cg.Hand(1)
    assert not hasattr(h2, "hand_c")
    assert not hasattr(h2, "id_hand")
    assert not hasattr(h2, "type_hand")
    assert not hasattr(h2, "is_hidden")
    assert cg.Hand.instance_count == 1
    assert len(cg.Hand.INSTANCE_LIST) == 1
    h3: cg.Hand = cg.Hand(2)
    assert hasattr(h3, "hand_c")
    assert hasattr(h3, "id_hand")
    assert hasattr(h3, "type_hand")
    assert hasattr(h3, "is_hidden")
    assert not h3.hand_c
    assert h3.id_hand == 2
    assert h3.type_hand == "player"
    assert h3.is_hidden == False
    assert cg.Hand.instance_count == 2
    assert len(cg.Hand.INSTANCE_LIST) == 2
    h4: cg.Hand = cg.Hand(3, is_hidden=True)
    assert hasattr(h4, "hand_c")
    assert hasattr(h4, "id_hand")
    assert hasattr(h4, "type_hand")
    assert hasattr(h4, "is_hidden")
    assert not h4.hand_c
    assert h4.id_hand == 3
    assert h4.type_hand == "player"
    assert h4.is_hidden == True
    assert cg.Hand.instance_count == 3
    assert len(cg.Hand.INSTANCE_LIST) == 3
    assert cg.Hand.INSTANCE_LIST[0] == h1
    assert cg.Hand.INSTANCE_LIST[1] == h3
    assert cg.Hand.INSTANCE_LIST[2] == h4
    noshow: CaptureResult[str] = capsys.readouterr()
    if noshow:
        pass


@pytest.mark.flaky(reruns=FLAKYRERUN, only_rerun=["HEYNOAH"])
def test_hand_print(
    setup: cg.Hand,
) -> None:
    h1_o: cg.Hand = setup
    assert "No Cards" in str(h1_o)
    h1: cg.Hand = rand_cards(h1_o)[0]
    checker: str = str(h1)
    for c in h1.hand_c:
        assert str(c) in checker
    assert len(str(h1).split(", ")) == len(h1.hand_c)
    h2: cg.Hand = cg.Hand(2, is_hidden=True)
    for _ in range(randint(1, 51)):
        h2.hand_c.append(cg.Card(choice(cg.Card.RANKS), choice(cg.Card.SUITS)))
    for c in h2.hand_c:
        assert str(c) not in str(h2), "HEYNOAH"


def test_hand_destroy(setup: cg.Hand) -> None:
    h1 = setup
    assert h1 in cg.Hand.INSTANCE_LIST
    assert len(cg.Hand.INSTANCE_LIST) == 1
    assert cg.Hand.instance_count == 1
    h1, to_add, count_card = rand_cards(h1)  # pyright: ignore[reportUnusedVariable]
    assert len(h1.hand_c) == count_card
    h1_copy: list[cg.Card] = h1.hand_c.copy()
    salvaged: list[cg.Card] = h1.destroy()
    assert len(salvaged) == count_card
    assert salvaged == h1_copy
    assert len(salvaged) == len(h1_copy)
    assert not h1.hand_c
    assert not cg.Hand.INSTANCE_LIST
    assert not cg.Hand.instance_count


def test_hand_shuffle(setup: cg.Hand) -> None:
    h1 = setup
    h1 = rand_cards(h1)[0]
    steps: int = randint(1, 50)
    h1_copy: list[cg.Card] = h1.hand_c.copy()
    h1.shuffle(steps)
    assert h1 != h1_copy
    assert len(h1.hand_c) == len(h1_copy)


def test_hand_take_cards_exact(
    setup: cg.Hand, capsys: pytest.CaptureFixture[str]
) -> None:
    h1_o: cg.Hand = setup
    h1: cg.Hand = rand_cards(h1_o, randint(27, 52))[0]
    h1_snap1: list[cg.Card] = h1.hand_c.copy()
    to_take: list[cg.Card] = h1.hand_c[
        randint(1, (len(h1.hand_c) // 2) - 1) : randint(
            len(h1.hand_c) // 2, len(h1.hand_c) - 1
        )
    ]
    assert len(to_take) <= len(h1.hand_c)
    h1_taken: list[cg.Card] = h1.take_cards_exact(to_take)
    assert h1_taken == to_take
    assert len(h1.hand_c) == len(h1_snap1) - len(h1_taken)
    assert set(h1_taken) not in set(h1.hand_c)
    assert h1.hand_c
    h2_o: cg.Hand
    h2_o = cg.Hand(2)
    h2_o = rand_cards(h2_o, randint(27, 52))[0]
    h2o_snap1: list[cg.Card] = h2_o.hand_c.copy()
    _deck: cg.Deck = cg.Deck("test")
    not_in_h2o: list[cg.Card] = [x for x in _deck.deck if x not in h2_o.hand_c]
    assert not_in_h2o not in h2_o.hand_c
    returned: list[cg.Card] = h2_o.take_cards_exact(not_in_h2o)
    assert not returned
    assert not_in_h2o not in h2_o.hand_c
    assert h2_o.hand_c == h2o_snap1
    noshow: CaptureResult[str] = capsys.readouterr()
    if noshow:
        pass


# This is fucking broken and I have no fucking idea how to fix it. At one point the actual main logic may be broken and another point the test is incorrect,
# and I don't know what were how when why.
# @pytest.mark.parametrize("n", [x for x in range(1)])
@pytest.mark.temp1
@pytest.mark.skip(reason="Review Hand Taken Logic.")
@pytest.mark.flaky(reruns=FLAKYRERUN, only_rerun=["HEYNOAH"])
def test_hand_take_cards(
    setup: cg.Hand,
    capsys: pytest.CaptureFixture[str],
    # n: int
) -> None:
    h1: cg.Hand = setup
    h1 = rand_cards(h1, randint(27, 52))[0]
    h1_snap1: list[cg.Card] = h1.hand_c.copy()
    rdtake: bool = choice([True, False])
    rdshuffle: bool = choice([True, False])
    count_take = randint(1, len(h1.hand_c) - 1)
    assert h1_snap1 == h1.hand_c
    taken_1: list[cg.Card] = h1.take_cards(count_take, rdtake, rdshuffle)
    assert taken_1
    assert len(taken_1) == count_take
    assert taken_1 not in h1.hand_c
    assert len(h1.hand_c) == len(h1_snap1) - len(taken_1)
    # Problematic code starts here
    if rdshuffle:
        assert h1_snap1 != h1.hand_c + taken_1, "HEYNOAH"
        assert [x for x in h1_snap1 if x not in taken_1] != h1.hand_c, "HEYNOAH"
    else:
        assert h1_snap1 == h1.hand_c + taken_1[::-1]
        assert h1.hand_c == h1_snap1[:-count_take]
    if rdtake:
        assert taken_1[::-1] != h1_snap1[-count_take:], "HEYNOAH"
    else:
        assert taken_1[::-1] == h1_snap1[-count_take:]
    # Ends here. Could take inspo from test_deck, but now I'm wondering if the tests there are also wrong and just always pass.
    h2: cg.Hand
    h2 = cg.Hand(2)
    h2 = rand_cards(h2, randint(27, 52))[0]
    h2_snap1 = h2.hand_c.copy()
    assert not h2.take_cards(len(h2.hand_c) + 1, False, False)
    assert h2.hand_c == h2_snap1
    noshow: CaptureResult[str] = capsys.readouterr()
    if noshow:
        pass


@pytest.mark.skip(reason="Review This")
def test_hand_put_cards(setup: cg.Hand, capsys: pytest.CaptureFixture[str]) -> None:
    h1: cg.Hand = setup
    put_list: list[cg.Card] = []
    for _ in range(randint(1, 52)):
        x: cg.Card = cg.Card(choice(cg.Card.RANKS), choice(cg.Card.SUITS))
        put_list.append(x)
    h1.put_cards(put_list)
    assert put_list in h1.hand_c
    h1_snap1 = h1.hand_c.copy()
    put_list2: list[cg.Card] = []
    for _ in range(len(h1.hand_c) - 1):
        put_list2.append(h1.hand_c[randint(0, len(h1.hand_c))])
    assert put_list2 in h1.hand_c
    h1.put_cards(put_list2)
    assert h1.hand_c == h1_snap1
    for card in put_list2:
        h1.hand_c.remove(card)
        assert card not in h1.hand_c


@pytest.mark.testreset
def test_xx() -> None:
    assert not cg.Hand.instance_count, "setup hand teardown failure"
    assert not cg.Hand.INSTANCE_LIST, "setup hand teardown failure"
