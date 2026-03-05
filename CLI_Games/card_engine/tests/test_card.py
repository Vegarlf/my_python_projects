"""Test Card Engine."""

import pytest

# from ..src import card_engine as cg
import card_engine as cg
from colorama import Fore
from string import ascii_uppercase, digits
import random
from collections.abc import Generator
from conftest import RUNCOUNT

pytestmark: pytest.MarkDecorator = pytest.mark.test_card


@pytest.fixture(params=[n for n in range(RUNCOUNT)])
def setup() -> Generator[tuple[str, str], None, None]:
    """Setup Card Engine."""
    cg.reset_game()
    randomrank: str = random.choice(cg.Card.RANKS)
    randomsuit: str = random.choice(cg.Card.SUITS)
    yield randomrank, randomsuit
    cg.reset_game()


@pytest.mark.parametrize(
    "input_rank_invalid, input_suit_invalid",
    [
        (
            random.choice(
                [c for c in (ascii_uppercase + str(digits)) if c not in cg.Card.RANKS]
            ),
            random.choice(
                [c for c in (ascii_uppercase + str(digits)) if c not in cg.Card.SUITS]
            ),
        ),
        (
            random.choice(
                [c for c in (ascii_uppercase + str(digits)) if c not in cg.Card.RANKS]
            ),
            random.choice(
                [c for c in (ascii_uppercase + str(digits)) if c not in cg.Card.SUITS]
            ),
        ),
    ],
)
def test_card_init(
    setup: tuple[str, str],
    input_rank_invalid: str,
    input_suit_invalid: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test Card Initialisation Validation."""
    rdrank, rdsuit = setup
    c1: cg.Card = cg.Card(input_rank_invalid, input_suit_invalid)
    noshow = capsys.readouterr()
    if noshow:
        pass
    assert not hasattr(c1, "rank")
    assert not hasattr(c1, "suit")
    assert not hasattr(c1, "card_str")
    ctemp: cg.Card = cg.Card(rdrank, rdsuit, is_temp=True)
    assert hasattr(ctemp, "rank")
    assert hasattr(ctemp, "suit")
    assert hasattr(ctemp, "card_str")
    cvalid: cg.Card = cg.Card(rdrank, rdsuit)
    assert hasattr(cvalid, "rank")
    assert hasattr(cvalid, "suit")
    assert hasattr(cvalid, "card_str")
    assert cg.Card.instance_count == 1


@pytest.mark.parametrize(
    "input_rank, red_suit, blue_suit,",
    [
        (
            random.choice(cg.Card.RANKS),
            random.choice(cg.Card.RED_SUITS),
            random.choice(cg.Card.BLUE_SUITS),
        ),
        (
            random.choice(cg.Card.RANKS),
            random.choice(cg.Card.RED_SUITS),
            random.choice(cg.Card.BLUE_SUITS),
        ),
    ],
)
def test_card_print(
    setup: tuple[str, str], input_rank: str, red_suit: str, blue_suit: str
) -> None:
    """Test Card Print."""
    rdrank, rdsuit = setup
    c_red: cg.Card = cg.Card(input_rank, red_suit)
    c_blue: cg.Card = cg.Card(input_rank, blue_suit)
    c_n_a: cg.Card = cg.Card(rdrank, rdsuit)
    assert Fore.RED in str(c_red) and Fore.BLUE in str(c_blue)
    assert not any(color in c_n_a.get_plain_string() for color in [Fore.RED, Fore.BLUE])


def test_card_eq(setup: tuple[str, str]) -> None:
    """Test Card __eq__ dunder."""
    rdrank, rdsuit = setup
    c1: cg.Card = cg.Card(rdrank, rdsuit)
    c2: cg.Card = cg.Card(rdrank, rdsuit)
    assert c1 == c2


@pytest.mark.testreset
def test_xx() -> None:
    assert not cg.Card.instance_count, "setup card teardown failure"
