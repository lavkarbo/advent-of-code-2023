import enum
import fileinput
from multiprocessing.managers import BaseListProxy


lines = [line.strip() for line in fileinput.input()]

images = [[]]
[images[-1].append(line) if line else images.append([]) for line in lines]


def print_image(image):
    for line in image:
        print(line)


def rotate_image(image):
    return ["".join(row[::-1]) for row in zip(*image)]


def reverse_str(line):
    return line[::-1]


def get_reflection_pattern(image: list[str], rotate=False) -> int:
    if rotate:
        image = rotate_image(image)
    n = len(image[0])
    for refl in range(1, n):
        length = min(refl, n - refl)
        if all(
            reverse_str(line[refl - length : refl]) == line[refl : refl + length]
            for line in image
        ):
            return refl
    return 0


tally = 0
for image in images:
    num = get_reflection_pattern(image)
    if num == 0:
        num = 100 * get_reflection_pattern(image, rotate=True)
        if num == 0:
            raise ValueError(f"Image doesn't have reflection. {image}")
    tally += num

print("Part 1:", tally)


def get_difference(list_1, list_2):
    count = 0
    if list_1 == list_2:
        return 0
    for l1, l2 in zip(list_1, list_2):
        for char1, char2 in zip(l1, l2):
            if char1 != char2:
                count += 1
    return count


def get_reflection_pt_2(image: list[str]) -> int:
    n = len(image)
    for i in range(1, n):
        search_height = min(i, n - i)
        above = image[i - search_height : i]
        below = image[i : i + search_height]
        # print(f"{i=} diff = {get_difference(above[::-1], below)}")
        # print(above[::-1])
        # print(below)
        # print()
        if get_difference(above[::-1], below) == 1:
            return i
    return 0


def remove_smudge(image):
    # image_copy = copy.deepcopy(image)
    for i, row in enumerate(image):
        for j, char in enumerate(row):
            new = "." if char == "#" else "#"
            image[i] = row[:j] + new + row[j + 1 :]
            # hor_reflections = get_reflection_pattern_pt_2(image)
            # hor_reflections = get_reflection_pattern_pt_2(image)
            if get_reflection_pattern(image) > 0:
                return image
            elif get_reflection_pattern(rotate_image(image)) > 0:
                return image
                # vert_reflections = get_reflection_pattern_pt_2(image_T)
                # if len(vert_reflections) + len(hor_reflections) == 2:
                #     return image
                # else:
                #     continue
            else:
                image[i] = row
    raise ValueError("No smudge gave reflection")


def get_vert_reflection_pattern(image):
    reflection_pattern = []
    n = len(image)
    for i, row in enumerate(image[1:]):
        if row == image[i - 1]:
            pass


def get_reflection_pattern_pt_2(image: list[str]) -> list[int]:
    reflection_pattern = []
    n = len(image[0])
    for refl in range(1, n):
        length = min(refl, n - refl)
        # for line in image:
        #     left = reverse_str(line[refl - length : refl])
        #     right = line[refl : refl + length]
        #     if left != right:
        #         break
        if all(
            reverse_str(line[refl - length : refl]) == line[refl : refl + length]
            for line in image
        ):
            reflection_pattern.append(refl)
    return reflection_pattern


def get_reflection_value(image: list[str]) -> int:
    value = 0
    value += 100 * get_reflection_pt_2(image)
    if value == 0:
        value += get_reflection_pt_2(rotate_image(image))
    if value == 0:
        raise ValueError(f"No reflection found for image:\n{image}")
    return value


def tests_pt_2():
    image_1 = [
        "#.##..##.",
        "..#.##.#.",
        "##......#",
        "##......#",
        "..#.##.#.",
        "..##..##.",
        "#.#.##.#.",
    ]

    image_2 = [
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]

    image_3 = [
        ".#..###..##.#",
        ".#..###..##.#",
        "##..#.###.###",
        "#.##...#..##.",
        "..####...#..#",
        "##..#..#.#...",
        "###..#.....##",
        "....##.##..#.",
        "....##.#...#.",
    ]

    image_4 = [
        "#####.#...###..",
        ".##.......##..#",
        "########.#.##..",
        "....###.#..##..",
        "....#...##.##..",
        ".........##...#",
        "#..##.####.###.",
        "#..##.####.###.",
        ".........##...#",
        "....#...##.##..",
        "....###.#..#...",
        "########.#.##..",
        ".##.......##..#"
    ]

    image_5 = [
        "###.##.",
        "###.##.",
        "#####.#",
        "..#.##.",
        "#..#..#",
        ".##....",
        "....##."
    ]

    assert get_reflection_value(image_3) == 800
    assert get_reflection_value(image_4) == 700

    assert get_reflection_value(image_1) == 300
    assert get_reflection_value(image_2) == 100

    print_image(rotate_image(image_5))
    assert get_reflection_value(image_5) == 5


tests_pt_2()

tally = 0
for image in images:
    tally += get_reflection_value(image)
    # tally += get_reflection_pt_2(image)


print("Part 2:", tally)
