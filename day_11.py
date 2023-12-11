import itertools
import re

import numpy as np


class Galaxy:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return f"Galaxy at {(self.row, self.col)}"

    def get_distance_to(self, other_galaxy: object) -> int:
        dy = abs(self.row - other_galaxy.row)
        dx = abs(self.col - other_galaxy.col)
        return dx + dy


def read_image(filename, expansion=True):
    with open(filename, "r") as f:
        lines = f.readlines()

    image_added_rows = []
    for line in lines:
        image_added_rows.append(line.strip())
        if line.find("#") == -1 and expansion:
            image_added_rows.append(line.strip())

    if not expansion:
        return image_added_rows

    image_transposed = ["".join(col) for col in zip(*image_added_rows)]
    image_expanded_transposed = []
    for col in image_transposed:
        image_expanded_transposed.append(col)
        if col.find("#") == -1:
            image_expanded_transposed.append(col)

    image_expanded = ["".join(row) for row in zip(*image_expanded_transposed)]

    return image_expanded


def part_1(filename):
    image = read_image(filename)
    galaxies = []
    for i, row in enumerate(image):
        matches = re.finditer(r"#", row)
        for match in matches:
            galaxies.append(Galaxy(i, match.start()))

    # for gal in galaxies:
    #     print(gal)

    distance = 0
    for galaxy1, galaxy2 in itertools.combinations(galaxies, 2):
        distance += galaxy1.get_distance_to(galaxy2)
    return distance


def load_galaxies(image, expansion_factor=1):
    rows_to_expand = []
    for i, row in enumerate(image):
        if row.find("#") == -1:
            rows_to_expand.append(i)
    cols_to_expand = []
    image_transposed = ["".join(col) for col in zip(*image)]
    for j, col in enumerate(image_transposed):
        if col.find("#") == -1:
            cols_to_expand.append(j)
    # print("Rows to expand:", rows_to_expand)
    # print("Cols to expand:", cols_to_expand)

    rows_to_expand = np.array(rows_to_expand)
    cols_to_expand = np.array(cols_to_expand)
    galaxies = []
    for i, row in enumerate(image):
        for m in re.finditer(r"#", row):
            n_rws_to_expand = len(rows_to_expand[rows_to_expand < i])
            n_cls_to_expand = len(cols_to_expand[cols_to_expand < m.start()])
            # print(
            #     (i, m.start()),
            #     n_rws_to_expand,
            #     n_cls_to_expand,
            # )
            row_index = i + (n_rws_to_expand) * (expansion_factor - 1)
            col_index = m.start() + (n_cls_to_expand) * (expansion_factor - 1)
            galaxies.append(Galaxy(row_index, col_index))
    return galaxies


def part_2(filename):
    image = read_image(filename, False)
    galaxies = load_galaxies(image, 1000000)
    # galaxies = []
    # for i, row in enumerate(image):
    #     matches = re.finditer(r"#", row)
    #     for match in matches:
    #         galaxies.append(Galaxy(i, match.start()))
    # for gal in galaxies:
    #     print(gal)

    distance = 0
    for galaxy1, galaxy2 in itertools.combinations(galaxies, 2):
        distance += galaxy1.get_distance_to(galaxy2)
    return distance


print("--- Part 1 ---")
print("Example  : ", part_1("input/day_11_example.txt"))
print("Real deal: ", part_1("input/day_11.txt"))

print("--- Part 2 ---")
print("Example  : ", part_2("input/day_11_example.txt"))
print("Real deal: ", part_2("input/day_11.txt"))
