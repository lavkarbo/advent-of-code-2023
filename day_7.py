import collections
import itertools
import re


def get_value_of_card(card: str) -> int:
    try:
        return int(card)  # A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
    except ValueError:
        if card == "T":
            return 10
        elif card == "J":
            return 11
        elif card == "Q":
            return 12
        elif card == "K":
            return 13
        elif card == "A":
            return 14
    raise KeyError(f"{card} is not a valid card")


class Hand:
    def __init__(self, cards: str, bid: int = 0) -> None:
        self.cards = cards
        self.bid = bid

    def rank(self) -> int:
        cards = self.cards
        unique_cards = len(set(cards))
        card_distribution = list(collections.Counter(cards).values())
        if unique_cards == 1:  # Five of a kind
            return 6
        elif 4 in card_distribution:  # Four of a kind
            return 5
        elif 3 in card_distribution and 2 in card_distribution:  # Full house
            return 4
        elif max(card_distribution) == 3:  # Three of a kind
            return 3
        elif unique_cards == 3:  # Two pair 23432
            return 2
        elif unique_cards == 4:  # One pair A23A4
            return 1
        elif unique_cards == 5:  # High card 23456
            return 0
        raise ValueError("Hand does not fall into one of the seven categories")

    def __str__(self) -> str:
        return self.cards

    def __eq__(self, other) -> bool:
        return self.cards == other.cards

    def __lt__(self, other) -> bool:
        if self.__eq__(other):
            return False
        if self.rank() == other.rank():
            for this_card, other_card in zip(self.cards, other.cards):
                this_value = get_value_of_card(this_card)
                other_value = get_value_of_card(other_card)
                if this_value == other_value:
                    continue
                elif this_value < other_value:
                    return True
                else:
                    return False
        return self.rank() < other.rank()


def import_hands(filename: str) -> list[Hand]:
    with open(filename, "r") as f:
        lines = f.readlines()
    return [Hand(hand, int(bid)) for hand, bid in (line.split() for line in lines)]


def part_1(filename):
    hands = import_hands(filename)
    hands_sorted = sorted(hands)
    tests_part_1()
    winnings = []
    for i, bid in enumerate([hand.bid for hand in hands_sorted]):
        winnings.append((i + 1) * bid)
    return [(i + 1) * hand.bid for i, hand in enumerate(hands_sorted)]


def tests_part_1():
    assert Hand("AAAAA").rank() == 6
    assert Hand("AA8AA").rank() == 5
    assert Hand("23332").rank() == 4
    assert Hand("TTT98").rank() == 3
    assert Hand("23432").rank() == 2
    assert Hand("A23A4").rank() == 1
    assert Hand("23456").rank() == 0

    assert Hand("33332") == Hand("33332")

    assert Hand("33332") > Hand("2AAAA")
    assert not Hand("33332") < Hand("2AAAA")
    assert Hand("77888") > Hand("77788")
    assert not Hand("77888") < Hand("77788")


print("Part 1 example: ", sum(part_1("input/day_7_example")))
print("Part 1:         ", sum(part_1("input/day_7")))


## Part 2


def get_value_of_card_part_2(card: str) -> int:
    try:
        return int(card)  # A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2 or J
    except ValueError:
        if card == "T":
            return 10
        elif card == "J":
            return 1
        elif card == "Q":
            return 12
        elif card == "K":
            return 13
        elif card == "A":
            return 14
    raise KeyError(f"{card} is not a valid card")


class Hand_2:
    def __init__(self, cards: str, bid: int = 0) -> None:
        self.cards = cards
        self.bid = bid
        self.joker_cards = self.get_joker_cards()

    def get_joker_cards(self) -> str:
        alts = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        joker_matches = re.finditer(r"J", self.cards)
        joker_positions = [match.start() for match in joker_matches]  # [1, 2] in QJJQ2
        all_alt_combinations = itertools.product(
            alts, repeat=len(joker_positions)
        )  # [[('A', 'A'), ('A', 'K'), ('A', 'Q'), ..]
        best_cards = self.cards
        best_hand = Hand(self.cards, self.bid)
        alt_cards = self.cards
        for alt_combination in all_alt_combinations:
            for i_hand, i_jokerpos in enumerate(joker_positions):
                alt_cards = (
                    alt_cards[:i_jokerpos]
                    + alt_combination[i_hand]
                    + alt_cards[i_jokerpos + 1 :]
                )
            alt_hand = Hand(alt_cards)
            if alt_hand.rank() > best_hand.rank():
                best_cards = alt_cards
                best_hand = alt_hand
        self.joker_cards = best_cards
        return best_cards

    def rank(self) -> int:
        cards = self.cards
        unique_cards = len(set(cards))
        card_distribution = list(collections.Counter(cards).values())
        if unique_cards == 1:  # Five of a kind
            return 6
        elif 4 in card_distribution:  # Four of a kind
            return 5
        elif 3 in card_distribution and 2 in card_distribution:  # Full house
            return 4
        elif max(card_distribution) == 3:  # Three of a kind
            return 3
        elif unique_cards == 3:  # Two pair 23432
            return 2
        elif unique_cards == 4:  # One pair A23A4
            return 1
        elif unique_cards == 5:  # High card 23456
            return 0
        raise ValueError("Hand does not fall into one of the seven categories")

    def joker_rank(self) -> int:
        cards = self.joker_cards
        unique_cards = len(set(cards))
        card_distribution = list(collections.Counter(cards).values())
        if unique_cards == 1:  # Five of a kind
            return 6
        elif 4 in card_distribution:  # Four of a kind
            return 5
        elif 3 in card_distribution and 2 in card_distribution:  # Full house
            return 4
        elif max(card_distribution) == 3:  # Three of a kind
            return 3
        elif unique_cards == 3:  # Two pair 23432
            return 2
        elif unique_cards == 4:  # One pair A23A4
            return 1
        elif unique_cards == 5:  # High card 23456
            return 0
        raise ValueError("Hand does not fall into one of the seven categories")

    def __str__(self) -> str:
        return self.cards

    def __eq__(self, other) -> bool:
        return self.cards == other.cards

    def __lt__(self, other) -> bool:
        if self.__eq__(other):
            return False
        if self.joker_rank() == other.joker_rank():
            for this_card, other_card in zip(self.cards, other.cards):
                this_value = get_value_of_card_part_2(this_card)
                other_value = get_value_of_card_part_2(other_card)
                if this_value == other_value:
                    continue
                elif this_value < other_value:
                    return True
                else:
                    return False
        return self.joker_rank() < other.joker_rank()


def tests_part_2():
    # New test:
    Hand_2("QJJQ2").get_joker_cards()

    assert get_value_of_card_part_2("J") == 1

    assert Hand_2("QJJQ2").joker_rank() == 5
    assert Hand_2("QQQQ2") > Hand_2("JKKK2")

    assert Hand_2("T55J5").joker_rank() == 5
    assert Hand_2("KTJJT").joker_rank() == 5
    assert Hand_2("QQQJA").joker_rank() == 5

    assert Hand_2("32T3K").joker_rank() == 1
    assert Hand_2("KK677").joker_rank() == 2
    assert Hand_2("T55J5").joker_rank() == 5
    assert Hand_2("KTJJT").joker_rank() == 5
    assert Hand_2("QQQJA").joker_rank() == 5

    assert Hand_2("32T3K") < Hand_2("KK677")
    assert Hand_2("KK677") < Hand_2("T55J5")
    assert Hand_2("T55J5") < Hand_2("KTJJT")
    assert Hand_2("QQQJA") < Hand_2("KTJJT")

    # Old test:
    assert Hand_2("AAAAA").rank() == 6
    assert Hand_2("AA8AA").rank() == 5
    assert Hand_2("23332").rank() == 4
    assert Hand_2("TTT98").rank() == 3
    assert Hand_2("23432").rank() == 2
    assert Hand_2("A23A4").rank() == 1
    assert Hand_2("23456").rank() == 0

    assert Hand_2("33332") == Hand_2("33332")

    assert Hand_2("33332") > Hand_2("2AAAA")
    assert not Hand_2("33332") < Hand_2("2AAAA")
    assert Hand_2("77888") > Hand_2("77788")
    assert not Hand_2("77888") < Hand_2("77788")

    part_2_winnings = part_2("input/day_7_example")
    assert sum(part_2_winnings) == 5905, f"Was {sum(part_2_winnings)}"


def import_hands_part_2(filename: str) -> list[Hand_2]:
    with open(filename, "r") as f:
        lines = f.readlines()
    return [Hand_2(hand, int(bid)) for hand, bid in (line.split() for line in lines)]


def part_2(filename):
    hands = import_hands_part_2(filename)
    hands_sorted = sorted(hands)
    tests_part_1()
    winnings = []
    for i, bid in enumerate([hand.bid for hand in hands_sorted]):
        winnings.append((i + 1) * bid)
    return [(i + 1) * hand.bid for i, hand in enumerate(hands_sorted)]


tests_part_2()
print("Part 2 example: ", sum(part_2("input/day_7_example")))
print("Part 2:         ", sum(part_2("input/day_7")))
