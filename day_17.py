import fileinput
from queue import PriorityQueue

grid = [[int(elem) for elem in row.strip()] for row in fileinput.input()]

path = [["." for _ in row] for row in grid]
# [print("".join(row)) for row in path]


def is_on_grid(x, y, grid):
    if min(x, y) < 0:
        return False
    if x >= len(grid):
        return False
    if y >= len(grid[0]):
        return False
    return True


def get_min_heatloss(n_min, n_max, grid):
    pq = PriorityQueue()
    pq.put((0, 0, 0, 1, 0, 0))  # heat, x, y, dx, dy, n_in_line
    pq.put((0, 0, 0, 0, 1, 0))  # heat, x, y, dx, dy, n_in_line
    visited = set()  # x, y, dx, dy, n_in_line
    heatloss = 0
    while pq:
        heatloss, x, y, dx, dy, n_in_line = pq.get()
        if x == len(grid) - 1 and y == len(grid[-1]) - 1:
            return heatloss
        if (x, y, dx, dy, n_in_line) in visited:
            continue
        visited.add((x, y, dx, dy, n_in_line))

        # Straight candidate:
        new_x = x + dx
        new_y = y + dy
        if (n_in_line < n_max) and is_on_grid(new_x, new_y, grid):
            pq.put((heatloss + grid[new_x][new_y], new_x, new_y, dx, dy, n_in_line + 1))

        # Left candidate:
        new_x = x - dy
        new_y = y + dx
        if n_in_line >= n_min and is_on_grid(new_x, new_y, grid):
            pq.put((heatloss + grid[new_x][new_y], new_x, new_y, -dy, dx, 1))

        # Right candidate:
        new_x = x + dy
        new_y = y - dx
        if n_in_line >= n_min and is_on_grid(new_x, new_y, grid):
            pq.put((heatloss + grid[new_x][new_y], new_x, new_y, dy, -dx, 1))


print("Part 1:", get_min_heatloss(1, 3, grid))


print("Part 2:", get_min_heatloss(4, 10, grid))
