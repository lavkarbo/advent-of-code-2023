from collections import defaultdict


def read_input(filename):
    with open(filename, "r") as f:
        return f.readlines()


def read_scratchcard(line):
    prefix, numbers = line.split(": ")
    card_number = int(prefix.split()[1])
    winning_string, drawn_string = numbers.split("|")

    winning_numbers = winning_string.split()
    drawn_numbers = drawn_string.split()
    return card_number, winning_numbers, drawn_numbers


def count_points(winning_numbers, drawn_numbers):
    points = 0
    winning = set(winning_numbers).intersection(set(drawn_numbers))
    if winning:
        points = 2 ** (len(winning) - 1)
    return points


def part_1(filename: str) -> None:
    all_lines = read_input((filename))
    all_points = []
    for line in all_lines:
        card_number, winning_numbers, drawn_numbers = read_scratchcard(line)
        points = count_points(winning_numbers, drawn_numbers)
        all_points.append((points))
    print(f"Points: {all_points}. Sum: {sum(all_points)}")


def count_winning(winning_numbers: list, drawn_numbers: list) -> int:
    winning = set(winning_numbers).intersection(set(drawn_numbers))
    return len(winning)


def count_copied_cards(cards: dict, card_number: int, count_winning_numbers: int) -> None:
    for card_offset in range(count_winning_numbers):
        next_card = int(card_number) + int(card_offset) + 1
        cards[next_card] += 1


def part_2(filename):
    all_lines = read_input((filename))
    cards = defaultdict(int)  # card_number: count
    for line in all_lines:
        card_number, winning_numbers, drawn_numbers = read_scratchcard(line)
        cards[card_number] += 1
        for _ in range(cards[card_number]):
            count_winning_numbers = count_winning(winning_numbers, drawn_numbers)
            count_copied_cards(cards, card_number, count_winning_numbers)

    print(f"Number of cards: {sum(cards.values())}")


def main():
    part_1("input/day_4_example")
    part_1("input/day_4")

    part_2("input/day_4_example")
    part_2("input/day_4")


if __name__ == "__main__":
    main()
