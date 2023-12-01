import re


def read_input(filename):
    with open(filename, "r") as f:
        return f.readlines()


def create_match_string(intstrings):
    digit_strings = []
    for key, value in intstrings.items():
        digit_strings.extend([key, str(value)])
    match_string = r"(" + '|'.join(digit_strings) + r")"
    return match_string


def convert_string_to_digit(string, string_to_integer):
    digit = string
    if len(string) > 1:
        digit = str(string_to_integer[string])
    return digit


def extract_first_and_last_int(line):
    line = line.strip()

    string_to_integer = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}
    match_string = create_match_string(string_to_integer)
    list_of_digits = re.findall(match_string, line)

    first, last = "not a", " number"
    first = convert_string_to_digit(list_of_digits[0], string_to_integer)
    last = convert_string_to_digit(list_of_digits[-1], string_to_integer)
    
    print(f"{line}: {first}, {last}")

    return int(first + last)


def main():
    all_lines = read_input("input/day_1")
    numbers = []
    for line in all_lines:
        number = extract_first_and_last_int(line)
        numbers.append(number)
    print(f"Sum of numbers: {sum(numbers)}")

if __name__ == "__main__":
    main()
