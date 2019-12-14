import collections
import copy

def print_value(value):
    global output_reg
    output_reg = value

def input_value():
    global input_reg
    return input_reg

def run_iter(memory):
    global last_pos
    global term_flag
    global last_base
    global input_flag
    relative_base = last_base
    i = last_pos
    while True:
        instr = [(memory[i] // 10**(4-k)) % 10 for k in range(5)]

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
            if input_flag:
                input_flag = False
            else:
                input_flag = True
                last_pos = i
                last_base = relative_base
                return

            if instr[2] == 0:
                res_idx = memory[i+1]
            elif instr[2] == 2:
                res_idx = relative_base + memory[i+1]
            else:
                raise RuntimeError("Invalid mode for op 3(parameter 1 for result)")

            memory[res_idx] = input_value()
            i += 2
            last_base = relative_base
            last_pos = i
            return

        elif instr[4] == 4: # output
            if instr[2] == 0:
                value = memory[memory[i + 1]]
            elif instr[2] == 2:
                value = memory[relative_base + memory[i+1]]
            else:
                value = memory[i + 1]
            print_value(value)
            i += 2
            last_pos = i
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
            break
        else:
            raise RuntimeError("Something went horribly wrong")

def find_tile(dict_pos):
    for key in dict_pos:
        if dict_pos[key] == 3:
            return key

def find_ball(dict_pos):
    for key in dict_pos:
        if dict_pos[key] == 4:
            return key

def find_move(dict_pos):
    global last_move
    x_tile, y_tile = find_tile(dict_pos)
    x_ball, y_ball = find_ball(dict_pos)
    if x_tile < x_ball:
        last_move = 1
        return 1
    if x_tile > x_ball:
        last_move = -1
        return -1
    return 0

def run_computer(memory_list):
    global term_flag
    global last_pos
    global last_base
    global input_reg
    global input_flag

    size = len(memory_list)
    memory_temp = {i : memory_list[i] for i in range(size)}
    memory_init = collections.defaultdict(int, memory_temp)
    memory = copy.deepcopy(memory_init)

    last_pos = 0
    last_base = 0
    term_flag = False
    dict_pos = collections.defaultdict(int)

    while not term_flag:
        run_iter(memory)
        x = output_reg
        run_iter(memory)
        y = output_reg
        run_iter(memory)
        dict_pos[(x,y)] = output_reg

    count = sum([dict_pos[key] == 2 for key in dict_pos])
    print("The number of distinct block tiles is", count)

    # 2nd part
    dict_pos = collections.defaultdict(int)
    memory = memory_init
    memory[0] = 2
    score = 0
    term_flag = False
    last_pos = 0
    last_base = 0
    input_flag = False

    while not term_flag:
        run_iter(memory)
        if term_flag:
            break

        if input_flag:
            input_reg = find_move(dict_pos)
            run_iter(memory)
        else:
            x = output_reg
            run_iter(memory)
            y = output_reg
            run_iter(memory)
            z = output_reg
            if x == -1 and y == 0:
                score = z
            else:
                dict_pos[(x,y)] = z

    print("The score is", score)


if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_computer(memory)
    except Exception as exc:
        print(exc)