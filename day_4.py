from collections import defaultdict
import regex as re


def read_input(filename):
    with open(filename, "r") as f:
        return f.readlines()


def read_scratchcard(line):
    prefix, numbers = line.split(": ")
    card_number = int(re.search(r"\d+", prefix).group())
    winning_string, drawn_string = numbers.split(" | ")
    winning_string = winning_string.strip()
    drawn_string = drawn_string.strip()

    winning_numbers = re.findall(r"\d+", winning_string)
    drawn_numbers = re.findall(r"\d+", drawn_string)
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
        line = line.strip()
        card_number, winning_numbers, drawn_numbers = read_scratchcard(line)
        points = count_points(winning_numbers, drawn_numbers)
        all_points.append((points))
    print(f"Points: {all_points}. Sum: {sum(all_points)}")


def count_numbers_correct(winning_numbers, drawn_numbers):
    winning = set(winning_numbers).intersection(set(drawn_numbers))
    return len(winning)


def part_2(filename):
    all_lines = read_input((filename))
    cards = defaultdict(int)  # card_number: count
    for line in all_lines:
        line = line.strip()
        card_number, winning_numbers, drawn_numbers = read_scratchcard(line)
        cards[card_number] += 1
        for _ in range(cards[card_number]):
            numbers_correct = count_numbers_correct(winning_numbers, drawn_numbers)
            for card_offset in range(numbers_correct):
                next_card = int(card_number) + int(card_offset) + 1
                cards[next_card] += 1
    for card_number, count in cards.items():
        print(f"Card {card_number}: {count}")
    print(f"Number of cards: {sum(cards.values())}")


def main():
    # part_1("input/day_4_example")
    # part_1("input/day_4")

    part_2("input/day_4_example")
    part_2("input/day_4")


if __name__ == "__main__":
    main()
