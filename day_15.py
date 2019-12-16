import collections
import sys

'''
last_idx, last_base, output_reg, input_reg, term_flag
empty_field, wall, oxygen_system
'''

def input_value():
    global input_reg
    return input_reg

def print_value(value):
    global output_reg
    output_reg = value

def run_iter(memory):
    global last_idx, last_base, term_flag
    relative_base = last_base
    i = last_idx
    while True:
        instr = [(memory[i] // 10**(4-k)) % 10 for k in range(5)]
        #print(instr)

        if instr[4] == 1 or instr[4] == 2: # add or multiply
            if instr[2] == 0:
                left_val = memory[memory[i+1]]
            elif instr[2] == 2:
                left_val = memory[relative_base + memory[i+1]]
            else:
                left_val = memory[i+1]

            if instr[1] == 0:
                right_val = memory[memory[i+2]]
            elif instr[1] == 2:
                right_val = memory[relative_base + memory[i + 2]]
            else:
                right_val = memory[i+2]

            if instr[0] == 0:
                res_idx = memory[i+3]
            elif instr[0] == 2:
                res_idx = relative_base + memory[i+3]
            else:
                raise RuntimeError("Invalid mode for op 1/2(parameter 1 for result)")

            if instr[4] == 1:
                memory[res_idx] = left_val + right_val
            else:
                memory[res_idx] = left_val * right_val
            i += 4

        elif instr[4] == 3: # input
            if instr[2] == 0:
                res_idx = memory[i+1]
            elif instr[2] == 2:
                res_idx = relative_base + memory[i+1]
            else:
                raise RuntimeError("Invalid mode for op 3(parameter 1 for result)")

            memory[res_idx] = input_value()
            i += 2

        elif instr[4] == 4: # output
            if instr[2] == 0:
                value = memory[memory[i + 1]]
            elif instr[2] == 2:
                value = memory[relative_base + memory[i+1]]
            else:
                value = memory[i + 1]
            print_value(value)
            i += 2
            last_idx = i
            last_base = relative_base
            return

        elif instr[4] == 5 or instr[4] == 6: # jump if true/false
            if instr[2] == 0:
                test_bit = memory[memory[i+1]]
            elif instr[2] == 2:
                test_bit = memory[relative_base + memory[i+1]]
            else:
                test_bit = memory[i + 1]

            jump_if_true = (instr[4] == 5)
            jump_if_false = not jump_if_true
            if (test_bit == 0 and jump_if_true) or (test_bit != 0 and jump_if_false):
                i += 3
                continue

            if instr[1] == 0:
                jump_address = memory[memory[i+2]]
            elif instr[1] == 2:
                jump_address = memory[relative_base + memory[i+2]]
            else:
                jump_address = memory[i+2]

            i = jump_address

        elif instr[4] == 7 or instr[4] == 8: # less-than / equals
            if instr[2] == 0:
                first_param = memory[memory[i+1]]
            elif instr[2] == 2:
                first_param = memory[relative_base + memory[i+1]]
            else:
                first_param = memory[i+1]

            if instr[1] == 0:
                second_param = memory[memory[i+2]]
            elif instr[1] == 2:
                second_param = memory[relative_base + memory[i+2]]
            else:
                second_param = memory[i+2]

            if instr[0] == 0:
                res_idx = memory[i+3]
            elif instr[0] == 2:
                res_idx = memory[i+3] + relative_base
            else:
                raise RuntimeError("Invalid mode for op 3(parameter 1 for result)")

            less_than_flag = (instr[4] == 7)
            if (less_than_flag and first_param < second_param) or (not less_than_flag and first_param == second_param):
                memory[res_idx] = 1
            else:
                memory[res_idx] = 0

            i += 4

        elif instr[4] == 9 and instr[3] == 0: # relative_base
            if instr[2] == 1:
                relative_base += memory[i+1]
            elif instr[2] == 0:
                relative_base += memory[memory[i+1]]
            else:
                relative_base += memory[relative_base + memory[i+1]]
            i += 2

        elif instr[4] == 9 and instr[3] == 9:
            term_flag = True
            return
        else:
            raise RuntimeError("Something went horribly wrong")

def step(direction, memory):
    global input_reg
    transform = [1, 4, 2, 3]
    real_direction = transform[direction]
    input_reg = real_direction
    run_iter(memory)

def scan_field(direction, memory):
    global input_reg, output_reg
    inv_direction = (direction + 2) % 4

    step(direction, memory)
    field_val = output_reg + 1
    if field_val != 1:
        step(inv_direction, memory)

    return field_val

def switch_branch(x_last, y_last, x_next, y_next, pointer_up, dx, dy, memory):
    x, y = x_last, y_last
    #print([x_last, y_last, x_next, y_next])

    while (x, y) != (0, 0):
        direction = pointer_up[(x, y)]
        inv_direction = (direction + 2) % 4
        step(inv_direction, memory)
        x, y = (x + dx[inv_direction]), (y + dy[inv_direction])

    second_part = []
    x, y = x_next, y_next

    while (x, y) != (0, 0):
        direction = pointer_up[(x, y)]
        inv_direction = (direction + 2) % 4
        second_part.append(direction)
        x, y = (x + dx[inv_direction]), (y + dy[inv_direction])

    for direction in reversed(second_part):
        step(direction, memory)


def bfs_find(x_init, y_init, field, visited, dx, dy, memory):
    global input_reg, output_reg, wall, oxygen_system, empty_field
    queue = collections.deque()
    pointer_up = {}

    queue.append((x_init, y_init))
    visited[(x_init, y_init)] = True
    field[(x_init, y_init)] = empty_field
    x_last, y_last = 0, 0

    while queue:
        x, y = queue.popleft()
        switch_branch(x_last, y_last, x, y, pointer_up, dx, dy, memory)
        x_last, y_last = x, y

        for direction in range(4):
            new_x, new_y = (x + dx[direction]), (y + dy[direction])
            if not visited[(new_x, new_y)]:
                field[(new_x, new_y)] = scan_field(direction, memory)
                if field[(new_x, new_y)] != wall:
                    visited[(new_x, new_y)] = True
                    pointer_up[(new_x, new_y)] = direction
                    queue.append((new_x, new_y))
                if field[(new_x, new_y)] == oxygen_system:
                    print("Found oxygen system at", [new_x, new_y])
                    oxy_loc = (new_x, new_y)

    print("Filled out map.")
    return oxy_loc


def bfs(x_init, y_init, field, dx, dy, start_flag):
    global wall, oxygen_system, empty_field
    inf = 10**9
    queue = collections.deque()
    visited = collections.defaultdict(bool)
    distance = collections.defaultdict(lambda : inf)
    visited[(x_init, y_init)] = True
    distance[(x_init, y_init)] = 0
    queue.append((x_init, y_init, 0))
    max_dist = 0

    while queue:
        x, y, cur_dist = queue.popleft()
        max_dist = max(max_dist, cur_dist)
        if field[(x, y)] == oxygen_system and start_flag:
            return cur_dist

        for direction in range(4):
            new_x, new_y = (x + dx[direction]), (y + dy[direction])
            if not visited[(new_x, new_y)] and field[(new_x, new_y)] != wall:
                distance[(new_x, new_y)] = cur_dist + 1
                visited[(new_x, new_y)] = True
                queue.append((new_x, new_y, cur_dist + 1))

    if not start_flag:
        return max_dist
    raise RuntimeError("Never should be here")


def two_pass_bfs(x_init, y_init, memory):
    global wall, oxygen_system
    inf = 10**9
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    transform = [1, 4, 2, 3]

    field = collections.defaultdict(int)
    visited = collections.defaultdict(bool)

    x_oxy, y_oxy = bfs_find(x_init, y_init, field, visited, dx, dy, memory)
    return x_oxy, y_oxy, bfs(x_init, y_init, field, dx, dy, True), bfs(x_oxy, y_oxy, field, dx, dy, False)


def run_program(memory):
    global input_reg, output_reg, term_flag, empty_field, wall, oxygen_system, last_base, last_idx, term_flag
    inf = 10**9
    wall, empty_field, oxygen_system = 1, 2, 3
    last_base = 0
    last_idx = 0
    term_flag = False
    x_oxy, y_oxy, distance_oxy, time_oxy = two_pass_bfs(0, 0, memory)
    print("The minimum distance to the oxygen system at", [x_oxy, y_oxy], "is", distance_oxy)
    print("It will take", time_oxy, "minutes for the ship to fill with oxygen")

if __name__ == "__main__":
    sys.setrecursionlimit(10**6)
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_program(memory)
    except Exception as exc:
        print(exc)