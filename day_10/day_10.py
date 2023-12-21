import re
import numpy as np
import math


def get_possible_directions(pipe):
    if pipe == "F":
        return (0, 1), (1, 0)
    elif pipe == "-":
        return (0, -1), (0, 1)
    elif pipe == "7":
        return (0, -1), (1, 0)
    elif pipe == "|":
        return (-1, 0), (1, 0)
    elif pipe == "J":
        return (-1, 0), (0, -1)
    elif pipe == "L":
        return (0, 1), (-1, 0)
    else:
        raise ValueError(f"{pipe} is not a valid pipe")


def is_on_map(dest, map_array):
    if min(dest) < 0:
        return False
    elif dest[0] >= len(map_array):
        return False
    elif dest[1] >= len(map_array[0]):
        return False
    return True


def get_move_from_start(start_pos, map_array):
    for r, c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        candidate_pos = (start_pos[0] + r, start_pos[1] + c)
        if not is_on_map(candidate_pos, map_array):
            continue
        next_pipe = map_array[candidate_pos[0]][candidate_pos[1]]
        # print("Checking pos ", candidate_pos, next_pipe)
        try:
            dir_1, dir_2 = get_possible_directions(next_pipe)
            # print(next_pipe, dir_1, dir_2)
            possible_from_cand_1 = (
                candidate_pos[0] + dir_1[0],
                candidate_pos[1] + dir_1[1],
            )
            possible_from_cand_2 = (
                candidate_pos[0] + dir_2[0],
                candidate_pos[1] + dir_2[1],
            )
            # print(next_pipe, "leads to", possible_from_cand_1, possible_from_cand_2)
            if start_pos in (possible_from_cand_1, possible_from_cand_2):
                # print(
                #     next_pipe,
                #     candidate_pos,
                #     "leads to",
                #     possible_from_cand_1,
                #     possible_from_cand_2,
                # )
                # print("Pos", candidate_pos, "is valid")
                return candidate_pos
        except ValueError:
            continue
    raise ValueError(f"No valid move from start pos {start_pos}")


def get_next_position(
    current_pos: tuple[int, int],
    previous_pos: tuple[int, int] | None,
    map_array: list[str],
) -> tuple[int, int] | None:
    pipe = map_array[current_pos[0]][current_pos[1]]
    if pipe == "S":
        if previous_pos is None:
            return get_move_from_start(current_pos, map_array)
        else:
            return None  # End run
    dir_1, dir_2 = get_possible_directions(pipe)
    next1 = (current_pos[0] + dir_1[0], current_pos[1] + dir_1[1])
    next2 = (current_pos[0] + dir_2[0], current_pos[1] + dir_2[1])
    if next1 == previous_pos and is_on_map(next2, map_array):
        return next2
    elif next2 == previous_pos and is_on_map(next1, map_array):
        return next1
    else:
        raise ValueError(
            f"None of the possible next moves {next1, next2} are valid from current {pipe}{current_pos} "
        )


def read_map(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_start_pos(mymap):
    for r, row in enumerate(mymap):
        if "S" in row:
            return (r, row.index("S"))
    raise ValueError("No start pos in map")


def tests_1():
    mymap = read_map("input/day_10_example")
    dir1, dir2 = get_possible_directions("F")
    assert (0, 1) in (dir1, dir2) and (1, 0) in (dir1, dir2)
    dir1, dir2 = get_possible_directions("-")
    assert (0, 1) in (dir1, dir2) and (0, -1) in (dir1, dir2)
    dir1, dir2 = get_possible_directions("7")
    assert (1, 0) in (dir1, dir2) and (0, -1) in (dir1, dir2)
    dir1, dir2 = get_possible_directions("|")
    assert (1, 0) in (dir1, dir2) and (-1, 0) in (dir1, dir2)
    dir1, dir2 = get_possible_directions("J")
    assert (-1, 0) in (dir1, dir2) and (0, -1) in (dir1, dir2)
    dir1, dir2 = get_possible_directions("L")
    assert (-1, 0) in (dir1, dir2) and (0, 1) in (dir1, dir2)

    assert get_next_position((1, 2), (1, 1), mymap) == (1, 3)
    assert get_next_position((1, 3), (1, 2), mymap) == (2, 3)
    assert get_next_position((2, 3), (1, 3), mymap) == (3, 3)
    assert get_next_position((3, 3), (2, 3), mymap) == (3, 2)
    assert get_next_position((3, 2), (3, 3), mymap) == (3, 1)
    assert get_next_position((3, 1), (3, 2), mymap) == (2, 1)
    assert get_next_position((2, 1), (3, 1), mymap) == (1, 1)

    start = get_start_pos(mymap)
    assert start == (1, 1)
    assert get_move_from_start(start, mymap) in ((1, 2), (2, 1))

    assert is_on_map((0, 0), mymap)
    assert is_on_map((4, 4), mymap)
    assert not is_on_map((-1, 4), mymap)
    assert not is_on_map((5, 4), mymap)


def part_1(filename):
    mymap = read_map(filename)
    tests_1()

    start = get_start_pos(mymap)
    current = start
    previous = None
    count = 0
    while current is not None:
        # print("Current pos: ", current)
        next_pos = get_next_position(current, previous, mymap)
        previous = current
        current = next_pos
        count += 1
    return count // 2


def tests_2():
    assert (
        part_2("input/day_10_example") == 1
    ), f"{part_2('input/day_10_example')} is not 1"
    assert part_2("input/day_10_example2") == 4
    assert part_2("input/day_10_example2_2") == 8
    assert part_2("input/day_10_example2_3.txt") == 10


def part_2(filename):
    mymap = read_map(filename)

    start = get_start_pos(mymap)
    current = start
    previous = None

    path = []
    while current is not None:
        path.append(current)
        next_pos = get_next_position(current, previous, mymap)
        previous = current
        current = next_pos

    ground_points = []  # TODO: add non-.
    for r, row in enumerate(mymap):
        # cols = re.finditer(r"\.", row)
        for c in range(len(row)):
            point = (r, c)
            if point not in path:
                ground_points.append(point)
        # ground_points.extend([(r, col.start()) for col in cols])
    print("ground points", ground_points)

    # path_xs = np.array([point[1] for point in path])
    # path_ys = np.array([point[0] for point in path])
    # path_dxs = np.diff(path_xs)
    # path_dys = np.diff(path_ys)
    # print(list(zip(path_dxs, path_dys)))

    enclosed_points = []
    for ground_point in ground_points:
        # xs = path_xs - ground_point[1]
        # ys = path_ys - ground_point[0]
        # thetas = np.arctan2(ys, xs)
        # print(list(zip(xs, ys)))
        # d_angles = np.diff(thetas)

        angles = []
        for i in range(1, len(path)):
            y2 = path[i][0] - ground_point[0]
            x2 = path[i][1] - ground_point[1]
            y1 = path[i - 1][0] - ground_point[0]
            x1 = path[i - 1][1] - ground_point[1]
            # print((y1, x1), mymap[y1][x1], "->", (y2, x2), mymap[y2][x2])
            # print((ys[i - 1], xs[i - 1]), mymap[y1][x1], "->", (ys[i], xs[i]), mymap[y2][x2])

            # assert x1 == xs[i - 1]
            # assert y1 == ys[i - 1]
            # assert x2 == xs[i]
            # assert y2 == ys[i]
            theta1 = math.atan2(y1, x1)
            theta2 = math.atan2(y2, x2)
            # assert theta1 == thetas[i - 1], f"{theta1} is not equal to {thetas[i-1]}"
            # assert theta2 == thetas[i], f"{theta2} is not equal to {thetas[i]}"

            d_theta = theta2 - theta1
            # assert d_theta == d_angles[i-1], f"{d_theta} is not equal to {d_angles[i-1]}"

            if d_theta < -math.pi:
                d_theta += 2 * math.pi
            elif d_theta > math.pi:
                d_theta -= 2 * math.pi
            angles.append(d_theta)

        if abs(sum(angles)) > 0.001:
            print("Adding point", ground_point, sum(angles))
            enclosed_points.append(ground_point)

    return len(enclosed_points)


print("--- Part 1 ---")
print("Part 1 ex 1:", part_1("input/day_10_example"), "\n")
print("Part 1 ex 2:", part_1("input/day_10_example_2"), "\n")
print("Part 1:", part_1("input/day_10"), "\n")


print("--- Part 2 ---")
tests_2()
print("Part 2 ex 1:", part_2("input/day_10_example"), "\n")
print("Part 2 ex 1:", part_2("input/day_10_example2"), "\n")
print("Part 2 ex 2:", part_2("input/day_10_example2_2"), "\n")
print("Part 2 ex 2:", part_2("input/day_10_example2_3.txt"), "\n")
print("Part 2:", part_2("input/day_10"), "\n")
