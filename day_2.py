def read_input(filename):
    with open(filename, "r") as f:
        return f.readlines()


def possible_games_from_max(games, min_red, min_green, min_blue):
    possible_games = []
    for game_number, rounds in games.items():
        print(f"Game {game_number}: {rounds}")
        max_red, max_green, max_blue = 0, 0, 0
        for red, green, blue in rounds:
            if red>max_red: max_red = red
            if green>max_green: max_green = green
            if blue>max_blue: max_blue = blue

        print(f"{max_red=}, {max_green=}, {max_blue=}")
        if max_red<=min_red and max_green<=min_green and max_blue<=min_blue:
            possible_games.append(game_number)
    return possible_games


def get_game(line):
    line = line.strip()
    prefix, rounds_text = line.split(": ")
    _, game_number = prefix.split(" ")
    rounds_text = rounds_text.split("; ")
    rounds = []
    for round in rounds_text:
        round = round.split(", ")
        red, green, blue = 0, 0, 0
        for dies in round:
            if dies.endswith("red"):
                red = int(dies.split(" ")[0])
            if dies.endswith("green"):
                green = int(dies.split(" ")[0])
            if dies.endswith("blue"):
                blue = int(dies.split(" ")[0])
        rounds.append((red, green, blue))
    return int(game_number), rounds


def get_all_games(all_lines):
    games = dict()  # 1: ((red, green, blue), ...)
    for line in all_lines:
        game_number, rounds = get_game(line)
        games[game_number] = rounds
    return games


def part_1(filename):
    all_lines = read_input(filename)
    games = get_all_games(all_lines)
    possible_games = possible_games_from_max(games, 12, 13, 14)
    print()
    print(f"Sum of possible games: {sum(possible_games)}")
    print()


def get_power_of_games(games):
    powers = []
    for rounds in games.values():
        min_red, min_green, min_blue = 0, 0, 0
        for red, green, blue in rounds:
            if red>min_red: min_red = red
            if green>min_green: min_green = green
            if blue>min_blue: min_blue = blue
        powers.append(min_red*min_green*min_blue)
    return powers


def part_2(filename):
    all_lines = read_input(filename)
    games = get_all_games(all_lines)
    power_of_games = get_power_of_games(games)
    print()
    print(power_of_games)
    print(f"Sum of possible games: {sum(power_of_games)}")
    print()


def main():
    # part_1("input/day_2_example")
    # part_1("input/day_2")

    part_2("input/day_2_example")
    part_2("input/day_2")


if __name__ == "__main__":
    main()
