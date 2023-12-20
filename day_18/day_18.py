from operator import le
import matplotlib.pyplot as plt
import fileinput
from shapely.geometry import Polygon

instructions = [
    (d, int(l), c[1:-1]) for d, l, c in [row.split() for row in fileinput.input()]
]


def calculate_area(path, length_of_path):
    n = len(path)  # of path
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += path[i][0] * path[j][1]
        area -= path[j][0] * path[i][1]
    area = abs(area) / 2.0
    return int(area + length_of_path)


def get_path(directions, lengths):
    path = []
    x = 0
    y = 0
    length_of_path = 1
    for d, l in zip(directions, lengths):
        path.append((y, x))
        if d == "R":
            y += l
            length_of_path += l
        elif d == "L":
            y -= l
            pass
        elif d == "D":
            x += l
            length_of_path += l
        elif d == "U":
            x -= l
            pass
    return path, length_of_path


directions, lengths, _ = zip(*instructions)

path, length_of_path = get_path(directions, lengths)

print("Part 1:", calculate_area(path, length_of_path))

# print(f"{min_x=}, {max_x=}, {min_y=}, {max_y=}")
# xs, ys = zip(*path)
# min_x = min(xs)
# min_y = min(ys)
# max_x = max(xs)
# max_y = max(ys)
# path_adjusted = [(x - min_x, y - min_y) for (x, y) in path]
# polygon = Polygon(path)
# x, y = polygon.exterior.xy
# plt.plot(x, y)
# plt.gca().invert_yaxis()
# plt.gca().set_aspect("equal", adjustable="box")
# plt.gca().set_xticks(range(min_x, max_x + 1, 1))
# plt.gca().set_yticks(range(min_y, max_y + 1, 1))
# plt.gca().grid(visible=True)
# plt.show()


new_instr = [(int(s[-1]), int(s[1:-1], 16)) for _, _, s in instructions]
new_dirs_int, new_lengths = zip(*new_instr)
dirs = ["R", "D", "L", "U"]
new_dirs = [dirs[i] for i in new_dirs_int]


path, length_of_path = get_path(new_dirs, new_lengths)
print("Part 1:", calculate_area(path, length_of_path))
