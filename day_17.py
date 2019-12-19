import collections

# old_base, old_i, term_flag, output_reg, input_queue

def print_value(value):
    global output_reg
    output_reg = value

def input_value():
    global input_queue
    empty_flag = (len(input_queue) > 1)
    return input_queue.popleft(), empty_flag

def print_list(val_list):
    global input_queue
    for idx in range(len(val_list)):
        if idx < len(val_list) - 1:
            input_queue.append(ord(","))
        input_queue.append(val_list[idx])
    input_queue.append(ord("\n"))

def run_iter(memory):
    global old_base, old_i, term_flag
    relative_base = old_base
    i = old_i
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

            memory[res_idx], empty_flag = input_value()
            i += 2
            if empty_flag:
                old_i = i
                old_base = relative_base
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
            old_i = i
            old_base = relative_base
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

def is_scafold(field):
    return (field == "#" or field == "^" or field == ">" or field == "v" or field == "<")

def find_robot(field_map):
    for row_idx in range(len(field_map)):
        for col_idx in range(len(field_map[0])):
            if is_scafold(field_map[row_idx][col_idx]) and field_map[row_idx][col_idx] != '#':
                return row_idx, col_idx
    raise RuntimeError("No robot on map.")

def get_path(field_map, x_start, y_start):
    inf = 10**9
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    distance = [[inf]*field_map[0] for row in field_map]
    pointer_up = [[None]*field_map[0] for row in field_map]
    queue = collections.deque()
    distance[x_start][y_start] = 0
    queue.append((x_start, y_start))

    while queue:
        x_cur, y_cur = queue.pop()
        num_neighbor = 0

        for direction in range(4):
            x_new, y_new = (x_cur + dx[direction]), (y_cur + dy[direction])
            if is_scafold(field_map[x_new][y_new]):
                num_neighbor += 1
                if distance[x_new][y_new] > distance[x_cur][y_cur] + 1:
                    queue.append((x_new, y_new))
                    distance[x_new][y_new] = distance[x_cur][y_cur] + 1
                    pointer_up = direction

        if num_neighbor == 1 and (x_cur, y_cur) != (x_start, y_start):
            return x_cur, y_cur, pointer_up

def str_from_path(field_map):
    x_start, y_start = find_robot(field_map)
    x_end, y_end, pointer_up = get_path(field_map, x_start, y_start)
    x, y = x_end, y_end
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    reversed_str = []
    last_direction = None

    while (x, y) != (x_start, y_start):
        direction = pointer_up[x][y]
        if direction == last_direction:
            if (not reversed_str) or reversed_str[-1] == "L" or reversed_str[-1] == "R":
                reversed_str.append(1)
            else:
                reversed_str[-1] += 1
        else:
            if (direction + 1) % 4 == last_direction:
                reversed_str.append("L")
            else:
                reversed_str.append("R")

        inv_direction = direction + 2
        if inv_direction > 4:
            inv_direction -= 4
        (x, y) = (x + dx[inv_direction]), (y + dy[inv_direction])

    return reversed(reversed_str)

def generate_all(substr):
    set_part = {}
    if substr[0] != "L" and substr[0] != "R":
        for left_slice in range(1, substr[0]+1):
            new_substr = [left_slice] + substr[1:]
            set_part.add(new_substr)

    set_full = {}
    for part_str in set_part:
        set_full.add(part_str)
        if part_str[-1] != "L" and part_str[-1] != "R":
            for right_slice in range(1, part_str[-1]+1):
                new_substr = part_str[:-1] + [right_slice]
                set_full.add(new_substr)

    return set_full


def get_substrings(string, max_len):
    set_substr = {}
    for low_idx in range(len(string)):
        upper_bound = min(len(string), low_idx + max_len)
        for high_idx in range(low_idx+1, upper_bound):
            set_substr.add(string[low_idx:high_idx])

    # didn't take number endings into consideration
    new_set = {}
    for substr in set_substr:
        for part in generate_all(substr):
            new_set.add(part)

    return new_set

def unravel(str):
    list_form = []
    for element in str:
        if element != "L" and element != "R":
            list_form.extend([1] * element)
        else:
            list_form.append(element)
    return list_form

def partition(scafold, sub_list):
    inf = 10**9
    scafold = unravel(scafold)
    sub_list = list(map(unravel, sub_list))

    min_char = [inf for char in scafold]
    min_char.append(0) # dummy variable so that min_char[-1] = 0
    backtrack = [None for char in scafold]

    for i in range(len(scafold)-1):
        for sub_idx in range(3):
            len_sub = len(sub_list[sub_idx])
            if scafold[(i-len_sub+1) : i] == sub_list[sub_idx] and min_char[i-len_sub] + 1 < min_char[i]:
                min_char[i] = min_char[i-len_sub] + 1
                backtrack[i] = sub_idx

    reversed_partition = []
    cur_idx = len(scafold) - 2
    if min_char[cur_idx] == inf:  # no solution found
        return [], False

    while cur_idx != -1:
        sub_idx = backtrack[cur_idx]
        cur_idx = cur_idx - len(sub_list[sub_idx])
        reversed_partition.append(ord("A") + sub_idx)

    return reversed(reversed_partition), True


def find_partition(cur_map):
    max_len = 20
    scafold = str_from_path(cur_map)
    all_substr = get_substrings(scafold, max_len)

    for first_substr in all_substr:
        for second_substr in all_substr:
            for third_substr in all_substr:
                potential_solution, is_solution = partition(scafold, [first_substr, second_substr, third_substr])
                if is_solution and len(potential_solution) <= max_len:
                    solution = (potential_solution, first_substr, second_substr, third_substr)
                    return solution

    raise RuntimeError("Haven't found any solution.")

def run_program(memory_list):
    global old_base, old_i, term_flag, input_queue, output_reg
    size = len(memory_list)
    memory_temp = {i : memory_list[i] for i in range(size)}
    memory = collections.defaultdict(int, memory_temp)
    input_queue = collections.deque()

    old_base = 0
    old_i = 0
    term_flag = False
    cur_map = [[]]
    run_iter(memory)

    while not term_flag:
        next_char = chr(output_reg)
        if output_reg == 10:
            cur_map.append([])
        else:
            cur_map[-1].append(next_char)
        run_iter(memory)

    while not cur_map[-1]:
        cur_map.pop()

    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    sum_param = 0

    for row_idx in range(1, len(cur_map) - 1):
        for col_idx in range(1, len(cur_map[row_idx]) - 1):
            if not is_scafold(cur_map[row_idx][col_idx]):
                continue
            all_scafold = True
            for direction_idx in range(4):
                new_row = row_idx + dx[direction_idx]
                new_col = col_idx + dy[direction_idx]
                if not is_scafold(cur_map[new_row][new_col]):
                    all_scafold = False
                    break
            if all_scafold:
                sum_param += row_idx * col_idx

    print("The sum of calibration parameters is", sum_param)

    out_file = open("output.txt","w+")
    for line in cur_map:
        out_file.write(''.join(line))
        out_file.write("\n")

    term_flag = 0
    old_base = 0
    old_i = 0
    solution, first_pattern, second_pattern, third_pattern = find_partition(cur_map)

    print_list(solution)
    print_list(first_pattern)
    print_list(second_pattern)
    print_list(third_pattern)
    print_list(["n", "\n"])

    if memory[0] != 1:
        raise RuntimeError("Assumption is wrong(memory[0] != 1)", memory[0])
    memory[0] = 2

    dust = output_reg
    print("The amount of collected dust is", dust)



if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_program(memory)
    except Exception as exc:
        print(exc)