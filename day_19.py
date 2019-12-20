import collections
import copy


# EW EWW EWWWWW EWWWW
# This problem is eww.
# fuj fuj fuj fuj

def print_value(value):
    global output_reg
    output_reg = value

def input_value():
    global input_reg
    return input_reg.popleft()

def run_iter(memory):
    relative_base = 0
    i = 0
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
            break
        else:
            raise RuntimeError("Something went horribly wrong")

def leftmost_point(x_inter, y_inter, memory_temp):
    global input_reg, output_reg
    lower_bound, upper_bound = 0, x_inter

    while lower_bound != upper_bound:
        memory = collections.defaultdict(int, memory_temp)
        middle = (lower_bound + upper_bound) // 2
        input_reg.append(middle)
        input_reg.append(y_inter)
        run_iter(memory)
        if output_reg == 0:
            lower_bound = middle + 1
        else:
            upper_bound = middle
        #print("STATE", [middle, output_reg])

    return lower_bound, y_inter

def rightmost_point(x_inter, y_inter, memory_temp):
    global input_reg, output_reg
    inf = 10**5 + 1
    lower_bound, upper_bound = x_inter, inf

    while lower_bound != upper_bound:
        memory = collections.defaultdict(int, memory_temp)
        middle = (lower_bound + upper_bound) // 2
        input_reg.append(middle)
        input_reg.append(y_inter)
        run_iter(memory)
        if output_reg == 1:
            lower_bound = middle + 1
        else:
            upper_bound = middle

    return (lower_bound-1), y_inter

def fails(x, y, memory_temp):
    memory = collections.defaultdict(int, memory_temp)
    input_reg.append(x)
    input_reg.append(y)
    run_iter(memory)
    if output_reg == 1:
        return False
    return True

def check_validity(x_left, y_left, square_size, memory_temp):
    dx = [0, 0, square_size-1, square_size-1]
    dy = [0, -square_size+1, -square_size+1, 0]
    for direction in range(4):
        new_x = x_left + dx[direction]
        new_y = y_left + dy[direction]
        memory = collections.defaultdict(int, memory_temp)
        input_reg.append(new_x)
        input_reg.append(new_y)
        run_iter(memory)
        if output_reg == 0:
            #print("fails,", [new_x, new_y])
            return False
    return True


def run_program(memory_list):
    global input_reg, output_reg, term_flag, last_base, last_i
    size = len(memory_list)
    memory_temp = {i: memory_list[i] for i in range(size)}
    memory = collections.defaultdict(int, memory_temp)

    term_flag = False
    map_size = 20
    count_tractor = 0
    input_reg = collections.deque()
    str_map = ""

    for row_idx in range(map_size):
        for col_idx in range(map_size):
            memory = collections.defaultdict(int, memory_temp)
            input_reg.append(col_idx)
            input_reg.append(row_idx)
            run_iter(memory)
            count_tractor += output_reg
            if output_reg == 0:
                str_map += "."
            else:
                str_map += "#"
        str_map += "\n"

    print("The number of points affected by the tractor beam is", count_tractor)

    x_fuj, y_fuj = 4, 3
    square_size = 100
    last_diff = 0

    while True:
        x_left, y_left = leftmost_point(x_fuj, y_fuj, memory_temp)
        x_right, y_right = rightmost_point(x_fuj, y_fuj, memory_temp)

        if x_right - x_left + 1 > last_diff:
            print("Diff", last_diff, "clear")
            last_diff = x_right - x_left + 1

        if x_right - x_left + 1 >= square_size:
            if check_validity(x_left, y_left, square_size, memory_temp):
                print("The answer is at", [x_left, y_left - square_size + 1])
                break

        x_fuj = x_left + 1
        y_fuj = y_left + 1
        if fails(x_fuj, y_fuj, memory_temp):
            x_fuj = x_right
            y_fuj = y_right + 1


if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_program(memory)
    except Exception as exc:
        print(exc)
