import numpy as np
import matplotlib.pyplot as plt
import math
import re
import networkx as nx
from pyvis.network import Network as net


def read_input(filename: str) -> tuple[str, dict]:
    with open(filename, "r") as f:
        lines = f.readlines()
    instructions, mapstrings = lines[0].strip(), [line.strip() for line in lines[2:]]
    mymap = {}
    for line in mapstrings:
        elements = re.findall(r"[0-9A-Z]{3}", line)
        mymap[elements[0]] = tuple(elements[1:])
    # mymap = {
    #     elements[0]: elements[1:]
    #     for elements in [re.findall(r"[A-Z]{3}", line) for line in mapstrings]
    # }
    return instructions, mymap


def navigate_and_count_steps(start, ending_string, instructions, mymap):
    count = 0
    position = start
    while not position.endswith(ending_string):
        instr_index = count % len(instructions)
        instruction = instructions[instr_index]
        lr_index = 0 if instruction == "L" else 1
        position = mymap[position][lr_index]
        # print(instruction, ": found", position)
        count += 1

    return count


def part_1(filename):
    instructions, mymap = read_input(filename)
    count = navigate_and_count_steps("AAA", "ZZZ", instructions, mymap)
    return count


def tests_part_1():
    assert part_1("input/day_8_example") == 2
    assert part_1("input/day_8_example_2") == 6


print("--- part 1 ---")
print("Part 1 example:  ", part_1("input/day_8_example"))
print("Part 1 example 2:", part_1("input/day_8_example_2"))
print("Part 1:          ", part_1("input/day_8"))


## Part 2


def plot_graphs(periods):
    lcm = math.lcm(*periods)
    x = np.linspace(0, 1, 1000000)
    ys = [np.sin(x * 2 * np.pi*period) for period in periods]
    # plt.plot(x, ys[0])
    # plt.plot(x, ys[1])
    # plt.plot(x, ys[2])
    # plt.plot(x, ys[3])
    plt.plot(x, ys[0]*ys[1]*ys[2]*ys[3]*ys[4]*ys[5])
    plt.xlim(0.999, 1)
    plt.show()
    pass


def part_2(filename):
    instructions, mymap = read_input(filename)
    starting_positions = re.findall(r"[0-9A-Z]{2}A", ",".join(mymap.keys()))
    print("Starting positions:", starting_positions)

    graph = nx.Graph()
    for origin, destinations in mymap.items():
        for destination in destinations:
            graph.add_edge(origin, destination)

    net_graph = net(
        directed=True,
        width=1300,
        height=1000,
    )
    net_graph.from_nx(graph)
    net_graph.show_buttons(filter_=["physics"])
    net_graph.show("visualisations/graph.html")

    counts = []
    for start in starting_positions:
        count = navigate_and_count_steps(start, "Z", instructions, mymap)
        counts.append(count)
    lcm = math.lcm(*counts)
    print("periods:", *counts)
    print("Least common multiple:", lcm)

    plot_graphs(counts)
    return lcm


print("--- part 2 ---")
# print("Part 2 example:", part_2("input/day_8_example_3"))
print("Part 2:        ", part_2("input/day_8"))
