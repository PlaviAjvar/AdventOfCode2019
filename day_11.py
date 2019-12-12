import collections
last_pos = 0
last_base = 0
term_flag = False
output_reg = 0
input_reg = 0

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
    size = len(memory)
    relative_base = last_base
    i = last_pos
    while i < size:
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

def run_computer(memory_list, init_val):
    global term_flag
    global input_reg
    global last_pos
    global last_base

    size = len(memory_list)
    memory_temp = {i : memory_list[i] for i in range(size)}
    memory = collections.defaultdict(int, memory_temp)

    last_pos = 0
    last_base = 0

    x_cur = 0
    y_cur = 0
    dir_flag = 0
    x_dif = [1, 0, -1, 0]
    y_dif = [0, 1, 0, -1]

    term_flag = False
    dict_pos = collections.defaultdict(int)
    input_reg = init_val

    while not term_flag:
        run_iter(memory)
        if term_flag:
            break
        dict_pos[(x_cur, y_cur)] = output_reg

        run_iter(memory)
        if output_reg == 0:
            dir_flag = (dir_flag + 3) % 4
        else:
            dir_flag = (dir_flag + 1) % 4

        x_cur += x_dif[dir_flag]
        y_cur += y_dif[dir_flag]

        if (x_cur, y_cur) not in dict_pos or dict_pos[(x_cur, y_cur)] == 0:
            input_reg = 0
        else:
            input_reg = 1

    num_distinct = len(dict_pos)
    if init_val == 0:
        panel_type = "BLACK"
    else:
        panel_type = "WHITE"
    print("The number of distinct painted panels for", panel_type, "starting panel is", num_distinct)

    if init_val == 0:
        return

    # if it's white print the hull
    inf = 10**9
    max_x, max_y = -inf, -inf
    min_x, min_y = inf, inf
    for key in dict_pos.keys():
        max_x = max(max_x, key[0])
        max_y = max(max_y, key[1])
        min_x = min(min_x, key[0])
        min_y = min(min_y, key[1])

    output_file = open("output.txt", "w+")

    for x in range(max_x, min_x-1, -1):
        for y in range(min_y, max_y + 1):
            if dict_pos[(x, y)] == 0:
                panel_key = " "
            else:
                panel_key = "#"
            output_file.write(panel_key)
        output_file.write("\n")

    output_file.close()


if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_computer(memory, 0)
        run_computer(memory, 1)
    except Exception as exc:
        print(exc)