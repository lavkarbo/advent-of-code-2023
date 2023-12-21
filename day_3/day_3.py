import itertools
import regex as re


class Part_number:
    def __init__(self, number: int, row_number: int, column_range: range) -> None:
        self.number = number
        self.row_number = row_number
        self.column_range = column_range

    def __str__(self) -> str:
        return f"{self.number} at row {self.row_number}, positions {self.column_range}"

    def __eq__(self, other) -> bool:
        return (
            self.number == other.number
            and self.row_number == other.row_number
            and self.column_range == other.column_range
        )

    def __hash__(self) -> int:
        return hash(self.number * self.row_number * sum(self.column_range))

    def get_position(self):
        return self.column_range, self.row_number

    def is_on_position(self, row_numner, column_nummber):
        return row_numner == self.row_number and column_nummber in self.column_range


def read_input(filename: str) -> list:
    with open(filename, "r") as f:
        return f.readlines()


def get_neighbour_numbers(
    row_number: int, column_number: int, number_positions: dict
) -> list:
    neighbouring_numbers = []
    for row_offset, column_offset in itertools.product(range(-1, 2), repeat=2):
        row = row_number + row_offset
        col = column_number + column_offset
        try:
            number = number_positions[row, col]
            if number not in neighbouring_numbers:
                neighbouring_numbers.append(number)
        except KeyError:
            continue
    return neighbouring_numbers


def get_all_part_numbers(filename: str, number_positions: dict) -> list:
    part_numbers = []

    all_lines = read_input(filename)
    for row_number, line in enumerate(all_lines):
        line = line.strip()
        found_items = re.finditer(r"(?:(?!\d+|\.).)", line)
        for item in found_items:
            column_number = item.start()
            neighbour_numbers = get_neighbour_numbers(
                row_number, column_number, number_positions
            )
            for neighbour_number in neighbour_numbers:
                if neighbour_number not in part_numbers:
                    part_numbers.append(neighbour_number)

    return part_numbers


def add_number_to_positions(
    number: Part_number, row_number: int, column_range: range, number_positions: dict
) -> None:
    for column_number in column_range:
        number_positions[row_number, column_number] = number


def get_all_numbers(filename: str):
    numbers = []
    number_positions = dict()

    all_lines = read_input(filename)
    for row_number, line in enumerate(all_lines):
        line = line.strip()
        numbers_found = re.finditer(r"\d+", line)
        for match in numbers_found:
            column_range = range(match.start(), match.end())
            number = Part_number(int(match.group()), row_number, column_range)
            numbers.append(number)
            add_number_to_positions(number, row_number, column_range, number_positions)

    return numbers, number_positions


def get_non_part_numbers(all_numbers, part_numbers):
    non_part_numbers = set(all_numbers) - set(part_numbers)
    return non_part_numbers


def sum_of_numbers(numbers: list) -> int:
    sum = 0
    for number in numbers:
        sum += number.number
    return sum


def part_1(filename: str) -> None:
    all_numbers, number_positions = get_all_numbers(filename)
    part_numbers = get_all_part_numbers(filename, number_positions)
    sum = sum_of_numbers(part_numbers)
    print(f"Sum of non-part numbers: {sum}")
    print()


def get_gear_ratios(filename: str, number_positions: dict) -> list:
    gear_ratios = []

    all_lines = read_input(filename)
    for row_number, line in enumerate(all_lines):
        line = line.strip()
        found_items = re.finditer(r"\*", line)
        for item in found_items:
            column_number = item.start()
            neighbour_numbers = get_neighbour_numbers(
                row_number, column_number, number_positions
            )
            if len(neighbour_numbers) == 2:
                gear_ratio = neighbour_numbers[0].number * neighbour_numbers[1].number
                gear_ratios.append(gear_ratio)

    return gear_ratios


def part_2(filename):
    all_numbers, number_positions = get_all_numbers(filename)
    gear_rations = get_gear_ratios(filename, number_positions)
    print(f"Sum of gear rations: {sum(gear_rations)}")
    print()


def main():
    part_1("input/day_3_example")
    part_1("input/day_3")

    part_2("input/day_3_example")
    part_2("input/day_3")


if __name__ == "__main__":
    main()
