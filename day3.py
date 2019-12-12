def get_dist(wire):
    return int(wire[1:])

def intersect(up, side):
    if up[0] < min(side[1], side[2]) or up[0] > max(side[1], side[2]):
        raise("")
    if side[0] < min(up[1], up[2]) or side[0] > max(up[1], up[2]):
        raise("")
    return side[0], up[0]

def get_lines(full_wire):
    uplines, sidelines = [], []
    x, y = 0, 0
    total_steps = 0
    for wire in full_wire:
        step = get_dist(wire)
        total_steps += step
        if wire[0] == "U" or wire[0] == "D":
            if wire[0] == "D":
                step = -step
            x += step
            uplines.append([y, x-step, x, total_steps])
        else:
            if wire[0] == "L":
                step = -step
            y += step
            sidelines.append([x, y-step, y, total_steps])
    return uplines, sidelines

def step_num(up, side, x, y):
    up_steps = up[3] - abs(up[2] - x)
    side_steps = side[3] - abs(side[2] - y)
    return up_steps + side_steps

if __name__ == "__main__":
    file = open("input.txt","r")
    first_line, second_line = [line for line in file]
    first_wire = first_line.split(",")
    second_wire = second_line.split(",")

    uplines_first, sidelines_first = get_lines(first_wire)
    uplines_second, sidelines_second = get_lines(second_wire)
    min_dist = 10**10
    steps_intersect = 10**10

    for up in uplines_first:
        for side in sidelines_second:
            try:
                x, y = intersect(up, side)
                if not(x == 0 and y == 0):
                    min_dist = min(min_dist, abs(x) + abs(y))
                    steps_intersect = min(steps_intersect, step_num(up, side, x, y))
            except:
                pass

    for up in uplines_second:
        for side in sidelines_first:
            try:
                x, y = intersect(up, side)
                if not(x == 0 and y == 0):
                    min_dist = min(min_dist, abs(x) + abs(y))
                    steps_intersect = min(steps_intersect, step_num(up, side, x, y))
            except:
                pass

    print("The minimum distance is", min_dist)
    print("The fewest steps to reach an intersection is", steps_intersect)
