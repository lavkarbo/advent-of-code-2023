from itertools import product
import math
import sys


def read_input(filename):
    with open(filename) as f:
        lines = f.readlines()
    times = [int(n) for n in lines[0].split()[1:]]
    distances = [int(n) for n in lines[1].split()[1:]]
    return times, distances


times, distances = read_input(sys.argv[1])


def beats_winning_time(hold_time, winning_time, winning_distance):
    time_to_move = winning_time - hold_time
    distance = hold_time * time_to_move
    return distance > winning_distance


def get_winning_times(winning_time, winning_distance):
    winning_times = []
    for time in range(1, winning_time):
        if beats_winning_time(time, winning_time, winning_distance):
            winning_times.append(time)
    return winning_times


def part_1(winning_times: list[int], winning_distances: list[int]) -> list[int]:
    ways_to_win = []
    for winning_time, winning_distance in zip(winning_times, winning_distances):
        num_ways_to_win = len(get_winning_times(winning_time, winning_distance))
        ways_to_win.append(num_ways_to_win)
    return ways_to_win

    # return get_winning_times(winning_time, winning_distance)


# def part_1(winning_times: list[int], winning_distances: list[int]) -> list[int]:
#     return get_winning_times(winning_times[0], winning_distances[0])


print("1: ", math.prod(part_1(times, distances)))
# print("1: ", list(map(part_1, (times, distances))))


def join_numbers(times, distances):
    new_time = "".join([str(n) for n in times])
    new_distance = "".join([str(n) for n in distances])
    return int(new_time), int(new_distance)


def part_2(winning_times, winning_distances):
    new_time, new_distance = join_numbers(winning_times, winning_distances)
    return len(get_winning_times(new_time, new_distance))


print("2: ", part_2(times, distances))
