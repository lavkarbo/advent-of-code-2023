import numpy as np


def import_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    all_series_string = [line.split() for line in lines]
    series = [
        [int(element) for element in serie_string] for serie_string in all_series_string
    ]
    return series


def part_1(filename):
    series = import_input(filename)
    next_element = []
    for serie in series:
        arr = np.array(serie)
        last_elements = []
        # print("Start:", arr)
        while True:
            last_elements.append(arr[-1])
            arr = np.diff(arr)
            if all(elem == 0 for elem in arr) or len(arr) == 1:
                last_elements.append(arr[-1])
                break
        print(serie, ", next:", sum(last_elements))
        next_element.append(sum(last_elements))
    return sum(next_element)


def alternating_sum(elements):
    elems = [(-1)**i * n for i, n in enumerate(elements)]
    return sum(elems)


def part_2(filename):
    series = import_input(filename)
    previous_elements = []
    for serie in series:
        arr = np.array(serie)
        first_elements = []
        print("Start:", arr)
        while True:
            first_elements.append(arr[0])
            arr = np.diff(arr)
            print(arr)
            if all(elem == 0 for elem in arr) or len(arr) == 1:
                first_elements.append(arr[0])
                break
        # print(serie, ", previous:", alternating_sum(first_elements))
        previous_elements.append(alternating_sum(first_elements))
    return previous_elements


print("--- Part 1 ---")
assert part_1("input/day_9_example") == 114
print("Part 1 ex:", part_1("input/day_9_example"))
print("Part 1   :", part_1("input/day_9"))

print("\n--- Part 2 ---")
prev_elems = part_2("input/day_9_example")
assert sum(prev_elems) == 2

print("Part 2 ex:", prev_elems, sum(prev_elems))
prev_elems = part_2("input/day_9")
print("Part 2   :", sum(prev_elems))
