import numbers


def read_input(filename):
    with open(filename, "r") as f:
        return f.readlines()


def get_seeds(all_lines):
    seeds_string = all_lines[0].split(": ")
    return [int(x) for x in seeds_string[1].split()]


def initiate_tables(list_of_tables):
    tables = dict()
    for table_name in list_of_tables:
        tables[table_name] = dict()

    return tables


def load_numbers_to_table(table, source_start, destination_start, length):
    for offset in range(length):
        table[source_start + offset] = destination_start + offset
    return table


def load_table_from_input(all_lines, table_name, tables):
    table = tables[table_name]
    load_line = False
    for line in all_lines:
        line = line.strip()
        if line.startswith(table_name):
            load_line = True
            continue
        if load_line and not line:
            load_line = False
            break
        if load_line:
            destination_start, source_start, length = [int(x) for x in line.split()]
            end = source_start + length
            table[(source_start, end)] = destination_start - source_start
    return table


def print_table(table):
    for key, value in table.items():
        print(f"{key}: {value}")


def get_next_number(table, current_number):
    for source_range, offset in table.items():
        if current_number in range(source_range[0], source_range[1]):
            return current_number + offset
    return current_number


def get_location_from_seed(seed_number, chain_of_tables, tables):
    current_number = seed_number
    print(f"Start: {current_number}")
    for table_name in chain_of_tables:
        next_number = get_next_number(tables[table_name], current_number)
        current_number = next_number
        print(f"Found {current_number} in {table_name}")
    return current_number


def print_all_tables(chain_of_tables, tables):
    print("--- All tables: ---")
    for table_name in chain_of_tables:
        print(table_name)
        print_table(tables[table_name])
        print()


def print_all_tables_extensive(chain_of_tables, tables):
    print("--- All tables: ---")
    for table_name in reversed(chain_of_tables):
        print("-".join(reversed(table_name.split("-"))))
        table = tables[table_name]
        for destination_range, source_range in table.items():
            offset = source_range[0] - destination_range[0]
            for destination in range(destination_range[0], destination_range[1]):
                print(f"{destination}: {destination + offset}")
        print()


def get_locations(seeds, chain_of_tables, tables):
    locations = []
    for seed in seeds:
        location = get_location_from_seed(seed, chain_of_tables, tables)
        locations.append(location)
        # print(f"Seed {seed} leads to {location}")
    return locations


def part_1(filename: str) -> None:
    all_lines = read_input((filename))
    seeds = get_seeds(all_lines)
    print(f"Seeds: {seeds}")
    chain_of_tables = (
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    )
    tables = initiate_tables(chain_of_tables)

    for table_name in chain_of_tables:
        load_table_from_input(all_lines, table_name, tables)

    print_all_tables(chain_of_tables, tables)
    locations = get_locations(seeds, chain_of_tables, tables)

    print(f"\nMinimum of locations: {min(locations)}")


def load_table_from_input_part_two(all_lines, table_name, tables):
    table = tables[table_name]
    load_line = False
    for line in all_lines:
        line = line.strip()
        if line.startswith(table_name):
            load_line = True
            continue
        if load_line and not line:
            load_line = False
            break
        if load_line:
            destination_start, source_start, length = [int(x) for x in line.split()]
            source_end = source_start + length
            destination_end = destination_start + length
            table[(destination_start, destination_end)] = (source_start, source_end)
    return table


def get_previous_number(table, current_number):
    for source_range, destination_range in table.items():
        offset = source_range[0] - destination_range[0]
        if current_number in range(source_range[0], source_range[1]):
            return current_number - offset
    raise KeyError


def get_seeds_from_ranges(all_lines):
    seed_input = get_seeds(all_lines)
    seed_ranges = []
    for i in range(0, len(seed_input), 2):
        start = seed_input[i]
        length = seed_input[i + 1]
        end = start + length
        seed_range = range(start, end)
        seed_ranges.append(seed_range)
    return seed_ranges


def get_seed_from_location(location, chain_of_tables, tables):
    current_number = location
    # print(f"Start: {current_number}")
    for table_name in chain_of_tables:
        try:
            previous_number = get_previous_number(tables[table_name], current_number)
            # print(f"Found {previous_number} in {table_name}")
        except KeyError:
            # print(
            #     f"No number {current_number} found in in {table_name}. Continuing with {current_number}"
            # )
            previous_number = current_number
        current_number = previous_number
    return current_number


def seed_is_in_table(seed, seed_table):
    for soil_range, seed_range in seed_table.items():
        seed_start, seed_end = seed_range
        if seed in range(seed_start, seed_end):
            return True
    return False


def part_2(filename):
    print("\n--- Part 2 ---")
    all_lines = read_input((filename))

    seed_ranges = get_seeds_from_ranges(all_lines)
    chain_of_tables = (
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    )
    tables = initiate_tables(chain_of_tables)

    for table_name in chain_of_tables:
        load_table_from_input_part_two(all_lines, table_name, tables)

    print_all_tables(chain_of_tables, tables)
    # print_all_tables_extensive(chain_of_tables, tables)
    location_map = tables["humidity-to-location"]
    # for location_range in sorted(location_map):
    #     location_start, location_end = location_range
    #     # humidity_start, humidity_end = humidity_range
    #     # offset = location_range[0] - humidity_range[0]
    #     for location in range(location_start, location_end):
    #         # location = location + offset
    #         seed_number = get_seed_from_location(
    #             location, reversed(chain_of_tables), tables
    #         )
    #         if seed_is_in_table(seed_number, tables["seed-to-soil"]):
    #             print(f"Location {location} leads to seed {seed_number}")
    #             break
    #         else:
    #             continue

    for location in range(50):
        # location = location + offset
        seed_number = get_seed_from_location(
            location, reversed(chain_of_tables), tables
        )
        if seed_is_in_table(seed_number, tables["seed-to-soil"]):
            print(f"Location {location} leads to seed {seed_number}")
            # break
        else:
            continue
    seed = 56
    # print(seed_is_in_table(seed, tables["seed-to-soil"]))


def main():
    part_1("input/day_5_example")
    # part_1("input/day_5")

    part_2("input/day_5_example")
    # part_2("input/day_5")


if __name__ == "__main__":
    main()
