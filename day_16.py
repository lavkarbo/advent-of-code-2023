import fileinput
import itertools
import re
import numpy as np


contraption = [[elem for elem in row.strip()] for row in fileinput.input()]

for row in contraption:
    print("".join(row))


def get_next_positions(current, previous, tile):
    x1 = current[0]
    y1 = current[1]
    x0 = previous[0]
    y0 = previous[1]
    dir_in = (x1 - x0, y1 - y0)
    if tile == "/":
        return (x1 - dir_in[1], y1 + dir_in[0]), (x1 - dir_in[1], y1 + dir_in[0])
    elif tile == "\\":
        return (x1 + dir_in[1], y1 - dir_in[0]), (x1 + dir_in[1], y1 - dir_in[0])
    elif tile == "|" and abs(dir_in[1]) == 1:
        return (-dir_in[1], dir_in[0]), (dir_in[1], dir_in[0])
    elif tile == "-" and abs(dir_in[0]) == 1:
        return (-dir_in[1], dir_in[0]), (dir_in[1], dir_in[0])
    else:
        return (x1 + dir_in[0], y1 + dir_in[1]), (x1 + dir_in[0], y1 + dir_in[1])


def test_get_next_pos():
    assert (-1, 0) in get_next_positions((0, 0), (0, -1), "/")
    assert (1, 0) in get_next_positions((0, 0), (0, -1), "\\")
    assert get_next_positions((0, 0), (0, -1), "-") == ((0, 1), (0, 1))
    assert all(
        pos in get_next_positions((0, 0), (0, -1), "|") for pos in ((-1, 0), (1, 0))
    )

    assert get_next_positions((0, 0), (0, 1), "/") == ((1, 0), (1, 0))
    assert get_next_positions((0, 0), (0, 1), "\\") == ((-1, 0), (-1, 0))
    assert get_next_positions((0, 0), (0, 1), "-") == ((0, -1), (0, -1))
    assert all(
        pos in get_next_positions((0, 0), (0, 1), "|") for pos in ((-1, 0), (1, 0))
    )

    assert (0, -1) in get_next_positions((0, 0), (-1, 0), "/")
    assert (0, 1) in get_next_positions((0, 0), (-1, 0), "\\")
    assert all(
        pos in get_next_positions((0, 0), (-1, 0), "-") for pos in ((0, -1), (0, 1))
    )
    assert (1, 0) in get_next_positions((0, 0), (-1, 0), "|")

    assert (0, 1) in get_next_positions((0, 0), (1, 0), "/")
    assert (0, -1) in get_next_positions((0, 0), (1, 0), "\\")
    assert (pos in get_next_positions((0, 0), (1, 0), "-") for pos in ((0, -1), (0, 1)))
    assert (-1, 0) in get_next_positions((0, 0), (1, 0), "|")


def get_energized_tiles(start, previous):
    path = [["." for _ in range(len(row))] for row in contraption]
    visited = set()
    to_visit = [(start, previous)]
    while to_visit:
        current, previous = to_visit.pop(0)
        x1 = current[0]
        y1 = current[1]
        if (current, previous) in visited:
            continue
        if min(current) < 0 or x1 >= len(contraption) or y1 >= len(contraption[0]):
            continue
        visited.add((current, previous))
        x0 = previous[0]
        y0 = previous[1]
        dx = x1 - x0
        dy = y1 - y0
        path[x1][y1] = "#"
        tile = contraption[x1][y1]
        if tile == "/":
            next_pos = (x1 - dy, y1 - dx)
            to_visit.append((next_pos, current))
        elif tile == "\\":
            next_pos = (x1 + dy, y1 + dx)
            to_visit.append((next_pos, current))
        elif tile == "-" and abs(dx) == 1:
            next_pos = (x1 - dy, y1 - dx)  # TODO
            to_visit.append((next_pos, current))
            next_pos = (x1 + dy, y1 + dx)  # TODO
            to_visit.append((next_pos, current))
        elif tile == "|" and abs(dy) == 1:
            next_pos = (x1 - dy, y1 - dx)  # TODO
            to_visit.append((next_pos, current))
            next_pos = (x1 + dy, y1 + dx)  # TODO
            to_visit.append((next_pos, current))
        else:
            next_pos = (x1 + dx, y1 + dy)
            to_visit.append((next_pos, current))

        # print(f"{current} {tile} -> {next_pos}")
        previous = current
    return sum([len(re.findall(r"#", "".join(row))) for row in path])


print("Part 1:", get_energized_tiles((0, 0), (0, -1)))


# --- Part 2 ---

best = 0
for i, row in enumerate(contraption):
    start_left = (i, 0)
    previous_left = (i, -1)
    start_right = (i, len(row) - 1)
    previous_right = (i, len(row))
    # print(start_left, previous_left, contraption[start_left[0]][start_left[1]])
    # print(start_right, previous_right, contraption[start_right[0]][start_right[1]])
    points_left = get_energized_tiles(start_left, previous_left)
    points_right = get_energized_tiles(start_right, previous_right)
    if max(points_left, points_right) > best:
        best = max(points_left, points_right)


for j in range(len(contraption[0])):
    start_top = (0, j)
    start_btm = (len(contraption)-1, j)
    previous_top = (-1, j)
    previous_btm = (len(contraption), j)
    # print(start_top, previous_top, contraption[start_top[0]][start_top[1]])
    # print(start_btm, previous_btm, contraption[start_btm[0]][start_btm[1]])
    points_top = get_energized_tiles(start_top, previous_top)
    points_btm = get_energized_tiles(start_btm, previous_btm)
    if max(points_btm, points_top) > best:
        best = max(points_btm, points_top)

print("Part 2:", best)