from collections import defaultdict
import fileinput
from turtle import update


sequence = [row.strip().split(",") for row in fileinput.input()][0]

# print(sequence)


def my_hash(string):
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


assert my_hash("HASH") == 52


sum_pt1 = sum([my_hash(command) for command in sequence])
print("Part 1:", sum_pt1)


def remove_contents(label, boxes):
    box_number = my_hash(label)
    updated_content = []
    for content in boxes[box_number]:
        if content[0] != label:
            updated_content.append(content)
    boxes[box_number] = updated_content

    return boxes


def add_contents(label, focal_length, boxes):
    new_content = (label, focal_length)
    updated_contents = []
    for content in boxes[my_hash(label)]:
        if content[0] == label:
            updated_contents.append(new_content)
        else:
            updated_contents.append(content)
    if new_content not in updated_contents:
        updated_contents.append((label, focal_length))
    boxes[my_hash(label)] = updated_contents
    return boxes


def print_boxes(boxes):
    for key, val in boxes.items():
        if val:
            print(f"Box {key}: {val}")


def calculate_focus_power(box_number, slot_number, focal_length):
    return (box_number + 1) * (slot_number + 1) * focal_length


boxes = defaultdict(list)
for command in sequence:
    # print(f"After {command}")
    if "-" in command:
        label, _ = command.split("-")
        boxes = remove_contents(label, boxes)
        # print_boxes(boxes)
    elif "=" in command:
        label, focal_length = command.split("=")
        boxes = add_contents(label, int(focal_length), boxes)
        # print_boxes(boxes)

focus_power = 0
for box_number, contents in boxes.items():
    for slot_number, content in enumerate(contents):
        focus_power += calculate_focus_power(box_number, slot_number, content[1])


print("Part 2:", focus_power)