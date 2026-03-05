"""Test Configuration"""

import pytest

# from ..src import card_engine as cg
import card_engine as cg
from collections.abc import Generator

RUNCOUNT: int = 1
FLAKYRERUN = 1


@pytest.fixture(params=[n for n in range(RUNCOUNT)])
def setup() -> Generator[tuple[cg.Deck, list[cg.Card]], None, None]:
    """Setup Game State, Teardown Leftovers."""
    cg.reset_game()
    d = cg.Deck()
    pre = d.deck.copy()
    assert d.deck == pre
    yield d, pre
    cg.reset_game()
