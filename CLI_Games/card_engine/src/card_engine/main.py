"""CLI Card Engine.

======================================
A complete, object-oriented framework for generating, managing, and
manipulating playing cards in terminal-based environments.

NOTE: Repo Structure Must Remain Intact For Local Imports To Work.

Author: Daivik, 15<super>th</super> Feb, 2026
"""

# for all the different functions, cause they all operate on list[Card] for ease.
# do: readme
# do: doctests

import collections.abc as typ
from os import name, system  # pyright: ignore[reportDeprecated]
from random import randint
from random import shuffle as rdshuffle
from sys import exit
from typing import override

from colorama import Fore, Style
from colorama import init as clr_init

# Path fixing for imports
import utils.caesar_cipher as c_c  # * credit to the algorithms on GitHub for this

clr_init(autoreset=True)


def get_integer_input(
    prompt: str,
    error_msg: str = "Value must be a valid integer.",
    error_msg_min: str = "Value is too low.",
    error_msg_max: str = "Value is too high.",
    min_input: int = 0,
    max_input: int = 1000,
) -> int:
    """Validate Input, Only Accepts Integers In Range min_input to max_input (exclusive).

    Args:
        prompt (str): Message To Display For Input
        error_msg (str, optional): Standard Error Message To Print.
        Defaults to "Value must be a valid integer".
        error_msg_min (str, optional): Error Message Printed When Input Too Low.
        Defaults to "Value is too low".
        error_msg_max (str, optional): Error Message Printed When Input Too High.
        Defaults to "Value is too high".
        min_input (int, optional): Minimum Allowed Input.
        Defaults to 0.
        max_input (int, optional): Maximum Allowed Input.
        Defaults to 1000.

    Returns:
        int: User Input, As Integer

    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"Error: {error_msg}\nTry Again.\n")
            continue

        if value < min_input:
            print(f"Error: {error_msg_min}\nTry Again.\n")
            continue
        if value > max_input:
            print(f"Error: {error_msg_max}\nTry Again.\n")
            continue

        return value


class Card:
    """Class For Individual Playing Card.

    Global Attributes:
        SUITS: List Of Suits, Uppercase
        RANKS: List Of Ranks, Uppercase
        RED_SUITS: List Of Red Suits, Uppercase
        BLUE_SUITS: List Of Black/Blue Suits, Uppercase
        instance_count: Number Of Objects That Exist (Should ALWAYS Be 52)
        NOTE: instance_count is broken, do not depend on it
    Returns:
        None
    """

    SUITS: list[str] = [
        "H",
        "D",
        "S",
        "C",
    ]
    RANKS: list[str] = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "T",
        "J",
        "Q",
        "K",
        "A",
    ]
    RED_SUITS: list[str] = [
        "H",
        "D",
    ]
    BLUE_SUITS: list[str] = [
        "S",
        "C",
    ]
    instance_count: int = 0

    def __init__(
        self,
        rank: str,
        suit: str,
        is_temp: bool = False,
    ) -> None:
        """'Card' Class Initialiser.

        Args:
            rank (str): Rank Of Card. Must Be One Letter, Must Be In Card.RANKs
            suit (str): Suit Of Card. Must Be One Letter, Must Be In Card.SUITS
            is_temp (bool, optional): If True, Does Not Add To Instance Counter.
            Defaults to False.

        """
        if len(rank) != 1 or len(suit) != 1:
            print(f"Invalid Card Length: Rank '{rank}' | Suit: '{suit}'")
        if not (suit in Card.SUITS and rank in Card.RANKS):
            print(
                f"Invalid Card Rank And/Or Suit: Rank '{rank}' | Suit '{suit}'"  # noqa: E501
            )
        else:
            self.suit: str = suit
            self.rank: str = rank
            self.card_str: str = f"{self.rank}{self.suit}"
            if not is_temp:
                Card.instance_count += 1

    @override
    def __str__(self) -> str:
        """Print Cards, Automatically Color Coded According To Suit.

        Returns:
            str: Colored Card As RankSuit

        """
        return (
            f"{Fore.RED}{self.card_str}"
            if self.suit in Card.RED_SUITS
            else f"{Fore.BLUE}{self.card_str}"
        )

    @override
    def __repr__(self) -> str:
        """Return Card With Defined Rank And Suit.

        Returns:
            str: Rank: {rank} | Suit: {suit}

        """
        return f"Card Rank: {self.rank} | Suit: {self.suit}"

    @override
    def __eq__(
        self,
        other: object,
    ) -> bool:
        """Check If Cards Are Equal (Checks Rank And Suit).

        Args:
            other (object): Card Object Being Compared To

        Returns:
            bool: True If Rank And Suit Are Same For Both Objects.

        """
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    @override
    def __hash__(self) -> int:
        """Give Unique Hash To Each Card.

        Returns:
            int: hash ??.

        """
        return hash(
            (
                self.rank,
                self.suit,
            ),
        )

    def get_plain_string(self) -> str:
        """Return Plain String, Not Color Coded, For Safe Logic Checks.

        Returns:
            str: Card As RankSuit

        """
        return f"{self.rank}{self.suit}"


def string_cleaner(
    input_str: str,
) -> list[Card]:
    """Clean User Input Into Card Objects.

    Takes User Input For Cards, Splits By Commas, And Converts Each Individual
    String To Card Object If String Is Valid (Form RankSuit With Valid Letters/Digits).
    Does Not Stop Function For Invalid String, Simply Prints Error Message For Each One.

    Args:
        input_str (str): Raw Input String To Be Cleaned And Converted

    Returns:
        list[Card]: List Of Cleaned Card Objects (List Even For One Object.)

    """
    input_str = input_str.upper().strip().replace(",", " ")
    input_cards: list[str] = input_str.split()
    clean_cards: list[Card] = []
    for raw_card in input_cards:
        if len(raw_card) != 2:
            print(f"Invalid Card Length Of {raw_card}")
            continue
        if raw_card[0] not in Card.RANKS:
            print(f"Invalid Card Rank: {raw_card[0]} Of {raw_card}")
            continue
        if raw_card[1] not in Card.SUITS:
            print(f"Invalid Card Suit: {raw_card[1]} Of {raw_card}")
            continue
        clean_cards.append(
            Card(
                raw_card[0],
                raw_card[1],
                is_temp=True,
            ),
        )
    return clean_cards


class Deck:
    """Deck That Holds 52 Cards.

    Returns:
        None

    """

    instance_count: int = 0
    INSTANCE_LIST: list["Deck"] = []

    def __init__(
        self,
        idd: str = "def",
    ) -> None:
        """Deck That Holds 52 Cards.

        Args:
            idd (str): ID Identifying Deck, Deprecated Since Only One Deck Is Allowed.

        Returns:
            None

        """
        if Deck.instance_count != 0:
            print(f"Deck Already Exists With ID {Deck.INSTANCE_LIST[0].id}")
        else:
            self.id: str = idd
            self.deck: list[Card] = []
            Deck.instance_count += 1
            Deck.INSTANCE_LIST.append(self)
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    self.deck.append(
                        Card(
                            rank,
                            suit,
                        ),
                    )

    @override
    def __str__(self) -> str:
        """Return Each Card In Deck Joined And Color Coded.

        Returns:
            str: Cards Joined By ', '

        """
        if not self.deck:
            return f"{Fore.GREEN}No Cards In Deck."
        return ", ".join(card.__str__() for card in self.deck)

    def shuffle(
        self,
        steps: int = 5,
    ) -> None:
        """Shuffles Deck steps Number Of Times.

        Args:
            steps (int, optional): Number Of Times To Shuffle Deck. Defaults to 5.

        """
        for _ in range(steps):
            rdshuffle(self.deck)

    def take_cards(
        self,
        count: int,
        random_take: bool = False,
        shuffle_after: bool = False,
    ) -> list[Card]:
        # noinspection DuplicatedCode
        """Take count Cards From Deck.

        Takes count Cards From Deck, Randomly if random_take, And Shuffles Deck
        Afterward If shuffle_after.

        Args:
            count (int): Number Of Cards To Take
            random_take (bool, optional): Whether To Take Cards Randomly.
            Defaults to False.
            shuffle_after (bool, optional): Whether To Shuffle Deck After Taking Cards.
            Defaults to False.

        Returns:
            list[Card]: List Of Taken Card Objects.

        """
        if count > len(self.deck):
            print(f"Cannot Draw {count} cards. Deck ID: {self.id}")
            return []
        drawn: list[Card] = []
        if random_take:
            for _ in range(count):
                drawn.append(self.deck.pop(randint(0, (len(self.deck) - 1))))
        else:
            for _ in range(count):
                drawn.append(self.deck.pop())
        if shuffle_after:
            self.shuffle()
        return drawn

    def put_cards(
        self,
        cards: list[Card],
        shuffle_after: bool = True,
    ) -> None:
        """Place Cards In Deck.

        Place List Of Cards In Deck If Cards Do Not Already Exist.

        Args:
            cards (list[Card]): List Of Cards
            shuffle_after (bool, optional): Whether To Shuffle Deck After Placing.
            Defaults to True.

        """
        valid_cards: list[Card] = []
        for c in cards:
            if c in self.deck:
                print(f"Card {c} already in deck")
            else:
                valid_cards.append(c)
        self.deck.extend(valid_cards)
        if shuffle_after:
            self.shuffle()

    def search_card_loc_deck(
        self,
        search_target: list[Card],
    ) -> dict[Card, int | None]:
        """Find Indices of Target Cards In Deck.

        Takes List of Target Cards And Returns Dictionary Mapping Each Card
        To Its Integer Index In The Deck List Or None If Not Present.

        Args:
            search_target (list[Card]): List Of Card Objects To Find

        Returns:
            dict[Card, int | None]: Dictionary Of Card:Index Pairs.

        """
        result: dict[Card, int | None] = {}
        for c in search_target:
            if c in self.deck:
                result[c] = self.deck.index(c)
            else:
                result[c] = None
        return result


def encrypt_hand(
    input_list: list[Card],
    random_key: bool = True,
    given_key: int = 0,
) -> tuple[list[str], int]:
    """Encrypts Card Identifiers Using Caesar Cipher.

    Converts Each Card In List To Plain String And Applies Caesar Cipher
    Encryption Using Either A Random Key Or A Provided Integer Key.

    Args:
        input_list (list[Card]): List Of Card Objects To Encrypt
        random_key (bool, optional): Generate Random Key If True. Defaults to True.
        given_key (int, optional): Specific Key To Use. Defaults to 0.

    Returns:
        tuple[list[str], int]: Tuple Of (List Of Encrypted Strings, Used Key)

    """
    if not random_key and given_key == 0:
        print("random_key False and given_key default (0)")
        return [], 0
    if not input_list:
        print("input_list is empty")
        return [], 0
    key: int = randint(1, 1000) if random_key else given_key

    # Safety check for the imported cipher
    if c_c:
        out: list[str] = [c_c.encrypt(c.get_plain_string(), key) for c in input_list]
    else:
        out = [c.get_plain_string() for c in input_list]

    return (
        out,
        key,
    )


class Hand:
    """Hand Object Representing A Subset Of Cards.

    Attributes:
        instance_count: Total Number Of Hand Objects
        INSTANCE_LIST: List Of Pointers To All Hand Objects

    """

    instance_count: int = 0
    INSTANCE_LIST: list["Hand"] = []

    def __init__(
        self,
        idh: int,
        type_h: str = "player",
        is_hidden: bool = False,
    ) -> None:
        """Hand Object Representing A Subset Of Cards.

        Args:
            idh (int): Unique Integer ID For Hand
            type_h (str, optional): Type Of Hand. Defaults to "player".
            is_hidden (bool, optional): Whether To Hide/Encrypt Hand. Defaults to False.

        """
        _hehehaha = 0
        for h in Hand.INSTANCE_LIST:
            if h.id_hand == idh:
                print(f"Hand With Id {idh} already exists: {h.id_hand}")
                _hehehaha += 1
        if _hehehaha == 0:
            self.id_hand: int = idh
            self.type_hand: str = type_h
            self.hand_c: list[Card] = []
            self.is_hidden: bool = is_hidden
            Hand.instance_count += 1
            Hand.INSTANCE_LIST.append(self)

    @override
    def __str__(self) -> str:
        """Return Formatted String Of Cards In Hand.

        If is_hidden Is True, Returns Encrypted Strings And Keys Used.
        Otherwise, Returns Color Coded Card Strings.

        Returns:
            str: Card List Or Encryption Metadata

        """
        if not self.is_hidden:
            if not self.hand_c:
                return f"No Cards In Hand (ID: {self.id_hand})"
            return ", ".join(card.__str__() for card in self.hand_c)
        if not self.hand_c:
            return f"No Cards In Hand (ID: {self.id_hand})"
        enc_hand, key = encrypt_hand(self.hand_c)
        cipher_hand: str = ", ".join(enc_card for enc_card in enc_hand)
        return f"Encrypted Hand {self.id_hand}:\nHand: {cipher_hand} | Wrapped Key: {key % 52}"  # noqa: E501

    def destroy(self) -> list[Card]:
        """Clear Hand And Removes Instance From Global Registry.

        Copies All Cards Out Of Hand To Be Returned (Salvaged), Clears Internal
        List, And Decrements Global Instance Counters.

        Returns:
            list[Card]: List Of Salvaged Cards From The Destroyed Hand.

        """
        salvaged_cards: list[Card] = self.hand_c.copy()
        self.hand_c.clear()
        if self in Hand.INSTANCE_LIST:
            Hand.INSTANCE_LIST.remove(self)
            Hand.instance_count -= 1
        del self
        return salvaged_cards

    def shuffle(
        self,
        steps: int = 5,
    ) -> None:
        """Shuffles Hand steps Number Of Times.

        Args:
            steps (int, optional): Number Of Times To Shuffle. Defaults to 5.

        """
        for _ in range(steps):
            rdshuffle(self.hand_c)

    def take_cards_exact(
        self,
        cards: list[Card],
    ) -> list[Card]:
        """Remove Explicit Cards From Hand.

        Attempts To Pop Specific Card Objects From Hand List. Prints Error
        Message If A Requested Card Does Not Exist In Current Hand.

        Args:
            cards (list[Card]): List Of Cards To Find And Remove

        Returns:
            list[Card]: Successfully Removed Card Objects.

        """
        drawn: list[Card] = []
        if len(cards) > len(self.hand_c):
            print(f"Cannot Draw {len(cards)} Cards From {len(self.hand_c)} Deck.")
            return []
        for c in cards:
            if c not in self.hand_c:
                print(f"Card {c} not in hand.")
            else:
                drawn.append(self.hand_c.pop(self.hand_c.index(c)))
        return drawn

    # noinspection DuplicatedCode
    def take_cards(
        self,
        count: int,
        random_take: bool = False,
        shuffle_after: bool = False,
    ) -> list[Card]:
        """Remove count Cards From Hand.

        Args:
            count (int): Number Of Cards To Take
            random_take (bool, optional): Pick From Random Indices. Defaults to False.
            shuffle_after (bool, optional): Shuffle Remaining Hand. Defaults to False.

        Returns:
            list[Card]: Taken Card Objects.

        """
        if count > len(self.hand_c):
            print(f"Cannot Draw {count} cards. Hand ID: {self.id_hand}")
            return []
        drawn: list[Card] = []
        if random_take:
            for _ in range(count):
                drawn.append(self.hand_c.pop(randint(0, (len(self.hand_c) - 1))))
        else:
            for _ in range(count):
                drawn.append(self.hand_c.pop())
        if shuffle_after:
            self.shuffle()
        return drawn

    def put_cards(
        self,
        cards: list[Card],
    ) -> None:
        """Add List Of Cards To Hand.

        Args:
            cards (list[Card]): List Of Cards To Add

        """
        for c in cards:
            if c in self.hand_c:
                print(f"Card {c} already in hand")
            else:
                self.hand_c.append(c)

    def search_card_loc_hand(
        self,
        search_target: list[Card],
    ) -> dict[Card, int | None]:
        """Find Indices Of Target Cards In Hand.

        Args:
            search_target (list[Card]): Cards To Find

        Returns:
            dict[Card, int | None]: Card Object Keys Mapped To Index Values.

        """
        result: dict[Card, int | None] = {}
        for c in search_target:
            if c in self.hand_c:
                result[c] = self.hand_c.index(c)
            else:
                result[c] = None
        return result


def reset_game() -> None:
    """Reset Game State To Original Configuration.

    Clear All Card, Hand, and Deck Instance Counts.
    """
    Card.instance_count = 0
    for h in Hand.INSTANCE_LIST:
        h.hand_c.clear()
    Hand.INSTANCE_LIST.clear()
    Hand.instance_count = 0
    for d in Deck.INSTANCE_LIST:
        d.deck = []
    Deck.INSTANCE_LIST.clear()
    Deck.instance_count = 0


def clear_screen() -> None:
    """Clear Terminal Screen Based On Operating System."""
    _ = system("cls" if name == "nt" else "clear")  # pyright: ignore[reportDeprecated]


def get_hands_from_input(
    prompt: str,
    hands_dict: dict[str, Hand],
) -> list[Hand]:
    """Parse User ID Strings Into Hand Objects.

    Takes User String Input, Cleans It Into List Of ID Strings, And Looks
    Up Hand Objects In Dictionary Matching Those IDs.

    Args:
        prompt (str): Prompt For Input
        hands_dict (dict[str, Hand]): Active Hand Registry

    Returns:
        list[Hand]: List Of Successfully Found Hand Objects.

    """
    raw_input: str = input(prompt).strip()
    if not raw_input:
        return []
    id_list: list[str] = raw_input.replace(",", " ").split()
    found_hands: list[Hand] = []
    for h_id in id_list:
        hand: Hand | None = next(
            (v for v in hands_dict.values() if str(v.id_hand) == h_id), None
        )
        if hand:
            found_hands.append(hand)
        else:
            print(f"Hand ID '{h_id}' Not Found.")
    return found_hands


def handle_drawn_destination(cards: list[Card], hands_dict: dict[str, Hand]) -> None:
    """Direct Drawn Cards To Destination Selected By User.

    Forces User To Place Drawn Cards Into Either A Specific Hand Registry
    Or Back Into The Global Deck To Prevent Card Deletion Errors.

    Args:
        cards (list[Card]): List Of Cards Drawn
        hands_dict (dict[str, Hand]): Active Hand Registry

    """
    if not cards:
        return

    print(f"\n{Fore.GREEN}Drawn Cards: {Style.RESET_ALL}\
        {', '.join(str(c) for c in cards)}")
    print(f"{Fore.CYAN}Where would you like to place these cards?{Style.RESET_ALL}")
    print("1. A specific Hand")
    print("2. Back to the Deck")

    dest_choice = input(">>> ").strip()

    if dest_choice == "1":
        if not Hand.INSTANCE_LIST:
            print("No Hands Created.")
        else:
            target = get_hands_from_input("Enter Hand ID: ", hands_dict)
            if target:
                target[0].put_cards(cards)
                print(f"Placed cards in Hand {target[0].id_hand}")
            else:
                print(
                    f"{Fore.RED}Invalid Hand. Returning cards to Deck to prevent deletion.{Style.RESET_ALL}"  # noqa: E501
                )
                if Deck.INSTANCE_LIST:
                    Deck.INSTANCE_LIST[0].put_cards(cards)
                else:
                    print(
                        f"{Fore.MAGENTA}If You're Seeing This Message You Somehow "
                        + "Spectacularly Broke The Game Code, Because You Managed To "
                        + "Pull Cards Out Of Nowhere And Have Nowhere To Put Them. "
                        + "Enjoy Your Ghost Cards. (Reset The Game.)"
                    )
    else:
        if Deck.INSTANCE_LIST:
            Deck.INSTANCE_LIST[0].put_cards(cards)
            print("Returned cards to the main Deck.")
        else:
            print("No Deck Created.")


MENU: str = f"""
{Fore.CYAN}{Style.BRIGHT}======= Menu ========{Style.RESET_ALL}
{Fore.YELLOW}1..{Fore.WHITE}  Create Deck
{Fore.YELLOW}2..{Fore.WHITE}  Create Hand(s)
{Fore.YELLOW}3..{Fore.WHITE}  Delete Hand(s)
{Fore.YELLOW}4..{Fore.WHITE}  Shuffle Deck
{Fore.YELLOW}5..{Fore.WHITE}  Shuffle Hand(s)
{Fore.YELLOW}6..{Fore.WHITE}  Print Deck
{Fore.YELLOW}7..{Fore.WHITE}  Print Hand(s)
{Fore.YELLOW}8..{Fore.WHITE}  Find Card In Deck
{Fore.YELLOW}9..{Fore.WHITE}  View Hand IDs
{Fore.YELLOW}10..{Fore.WHITE} Draw From Deck
{Fore.YELLOW}11..{Fore.WHITE} Draw From Hand
{Fore.YELLOW}12..{Fore.WHITE} Place In Deck
{Fore.YELLOW}13..{Fore.WHITE} Place In Hand(s)
{Fore.YELLOW}14..{Fore.WHITE} Toggle Hand Encryption
{Fore.YELLOW}15..{Fore.WHITE} Reset Game
{Fore.YELLOW}16..{Fore.WHITE} Quit
{Fore.CYAN}{Style.BRIGHT}====================={Style.RESET_ALL}
"""


def main_loop() -> None:
    """Game Loop."""
    while True:
        if clear_screen_choice:
            clear_screen()
        print()
        print(f"{Fore.GREEN}{Style.BRIGHT} CLI Card Manager")
        print(f"{Fore.GREEN}=" * 30)
        print(MENU)

        menu_choice: str = input(f"{Fore.CYAN}>>>  {Style.RESET_ALL}").strip()

        if not menu_choice:
            continue

        match menu_choice:
            case "1":
                if Deck.instance_count >= 1:
                    print("Deck Already Made")
                else:
                    dck: Deck = Deck()
                    print(f"Created New Deck ID '{dck.id}'!")
            case "2":
                amount_raw = input(
                    "Enter Number Of Hands To Make (or Enter to back): "
                ).strip()
                if not amount_raw:
                    continue

                amount: int = get_integer_input(
                    prompt=f"Confirm Amount ({amount_raw}): ",
                    min_input=1,
                    max_input=10,
                )
                for _ in range(amount):
                    next_id: int = next(counter)
                    name_inner: str = input(
                        f"Name of Hand {next_id} (or Enter to go back):  "
                    ).strip()
                    if not name_inner:
                        break
                    active_hands[f"hand_{name_inner}"] = Hand(idh=next_id)
                print(f"Made {amount} Hands!")
            case "3":
                hands: list[Hand] = get_hands_from_input(
                    "IDs To Delete (or Enter to go back): ", active_hands
                )
                if not hands:
                    continue
                for h in hands:
                    key: str = next(k for k, v in active_hands.items() if v == h)
                    dropped: list[Card] = h.destroy()
                    del active_hands[key]
                    if Deck.INSTANCE_LIST:
                        Deck.INSTANCE_LIST[0].put_cards(dropped, shuffle_after=False)
                    print(f"Deleted Hand {h.id_hand}.")
            case "4":
                if Deck.INSTANCE_LIST:
                    Deck.INSTANCE_LIST[0].shuffle()
                    print("Deck Shuffled.")
                else:
                    print("No Deck created.")
            case "5":
                hands_to_shuf: list[Hand] = get_hands_from_input(
                    "IDs To Shuffle (or Enter to go back): ", active_hands
                )
                if not hands_to_shuf:
                    continue
                for h in hands_to_shuf:
                    h.shuffle()
                    print(f"Hand {h.id_hand} shuffled.")
            case "6":
                if Deck.INSTANCE_LIST:
                    print(Deck.INSTANCE_LIST[0])
                else:
                    print("No Deck created.")
            case "7":
                hands_to_print: list[Hand] = get_hands_from_input(
                    "IDs To Print (or Enter to go back): ", active_hands
                )
                if not hands_to_print:
                    continue
                for h in hands_to_print:
                    print(f"Hand {h.id_hand}: {h}")
            case "8":
                target: str = input("Cards To Find (or Enter to back): ").strip()
                if not target:
                    continue
                if Deck.INSTANCE_LIST:
                    results: dict[Card, int | None] = Deck.INSTANCE_LIST[
                        0
                    ].search_card_loc_deck(string_cleaner(target))
                    for card, pos in results.items():
                        print(f"{card}: {'Not found' if pos is None else f'Index {pos}'}")
            case "9":
                if not active_hands:
                    print("No active hands.")
                for k, v in active_hands.items():
                    print(f"Name: {k} | ID: {v.id_hand}")
            case "10":
                if not Deck.INSTANCE_LIST:
                    print("No Deck.")
                    continue
                spec: str = (
                    input("Specific Card? (Y/N or Enter to back): ").strip().upper()
                )
                if not spec:
                    continue
                drawn: list[Card] = []
                if spec == "Y":
                    spec_cards_raw = input("Enter cards (or Enter to back): ")
                    if not spec_cards_raw:
                        continue
                    to_draw: list[Card] = string_cleaner(spec_cards_raw)
                    for c in to_draw:
                        if c in Deck.INSTANCE_LIST[0].deck:
                            Deck.INSTANCE_LIST[0].deck.remove(c)
                            drawn.append(c)
                else:
                    amt_raw = input("Amount (or Enter to back): ").strip()
                    if not amt_raw:
                        continue
                    amt: int = int(amt_raw)
                    drawn = Deck.INSTANCE_LIST[0].take_cards(amt)

                handle_drawn_destination(drawn, active_hands)
            case "11":
                target_hand_draw: list[Hand] = get_hands_from_input(
                    "Hand ID to draw from (or Enter to back): ", active_hands
                )
                if target_hand_draw:
                    h_draw: Hand = target_hand_draw[0]
                    amt_raw = input("Amount to draw (or Enter to back): ").strip()
                    if not amt_raw:
                        continue
                    drawn_from_h = h_draw.take_cards(int(amt_raw))
                    handle_drawn_destination(drawn_from_h, active_hands)
            case "12":
                target_hand_deck: list[Hand] = get_hands_from_input(
                    "Hand ID (or Enter to back): ", active_hands
                )
                if target_hand_deck:
                    h_deck: Hand = target_hand_deck[0]
                    cards_to_deck: list[Card] = h_deck.destroy()
                    if Deck.INSTANCE_LIST:
                        Deck.INSTANCE_LIST[0].put_cards(cards_to_deck)
                        print("Cards returned to Deck.")
            case "13":
                target_hand_put: list[Hand] = get_hands_from_input(
                    "Hand ID (or Enter to back): ", active_hands
                )
                if target_hand_put:
                    h_put: Hand = target_hand_put[0]
                    raw_cards = input("Cards to put (or Enter to back): ")
                    if not raw_cards:
                        continue
                    cards_to_put: list[Card] = string_cleaner(raw_cards)
                    h_put.put_cards(cards_to_put)
            case "14":
                target_hand_enc: list[Hand] = get_hands_from_input(
                    "Hand ID (or Enter to back): ", active_hands
                )
                if target_hand_enc:
                    target_hand_enc[0].is_hidden = not target_hand_enc[0].is_hidden
                    print(f"Encryption {'ON' if target_hand_enc[0].is_hidden else 'OFF'}")
            case "15":
                reset_game()
                print("Game reset.")
            case "16":
                print(f"{Fore.GREEN}Goodbye.")
                exit()
            case _:
                print(f"{Fore.RED}Invalid input.")

        _ = input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    counter: typ.Generator[int, None, None] = (x for x in range(1, 1000))
    active_hands: dict[str, Hand] = {}
    clear_screen_choice: bool = False

    while True:
        choice: str = input("Clear screen every turn? (Y/N): ").strip().upper()
        if choice in [
            "Y",
            "N",
        ]:
            clear_screen_choice = choice == "Y"
            break
        print("Invalid choice.")

    main_loop()
