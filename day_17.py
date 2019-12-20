import collections

# bruh...

# old_base, old_i, term_flag, output_reg, input_queue

def print_value(value):
    global output_reg
    output_reg = value

def input_value():
    global input_queue
    empty_flag = (len(input_queue) > 1)
    return input_queue.popleft(), empty_flag

def print_list(values):
    global input_queue
    strr = ""
    for idx in range(len(values)):
        if idx > 0:
            input_queue.append(ord(","))
            strr += ","
        if values[idx] == "L" or values[idx] == "R":
            input_queue.append(ord(values[idx]))
            strr += values[idx]
        else:
            helper = values[idx]
            for char in str(helper):
                strr += char
                input_queue.append(ord(char))
    input_queue.append(ord("\n"))
    print(strr)
    print(input_queue)

def run_iter(memory):
    global old_base, old_i, term_flag, empty_flag
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

def get_direction(field):
    if field == "^":
        return 0
    if field == ">":
        return 1
    if field == "<":
        return 3
    return 2

def get_path(field_map):
    x_start, y_start = find_robot(field_map)
    row_count = len(field_map)
    col_count = len(field_map[0])
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    x, y = x_start, y_start
    direction = get_direction(field_map[x_start][y_start])
    path = []

    while True:
        #print(path)
        #print(direction, [x,y])
        has_neighbor = False
        for pseudo_dir in range(direction, direction + 4):
            dir = pseudo_dir % 4
            x_new, y_new = (x + dx[dir]), (y + dy[dir])
            if x_new < 0 or y_new < 0 or x_new >= row_count or y_new >= col_count:
                continue

            if is_scafold(field_map[x_new][y_new]):
                if dir == (direction + 1) % 4:
                    path += "R"
                if dir == (direction + 3) % 4:
                    path += "L"
                if dir == direction or dir == (direction + 1) % 4 or dir == (direction + 3) % 4:
                    if not path or path[-1] == "L" or path[-1] == "R":
                        path.append(1)
                    else:
                        path[-1] += 1
                    has_neighbor = True
                    x, y = x_new, y_new
                    direction = dir
                    break

        if not has_neighbor:
            return path

    raise("There should always be a path")

def unravel(str):
    list_form = []
    for element in str:
        if element != "L" and element != "R":
            list_form.extend([1] * element)
        else:
            list_form.append(element)
    return list_form

def partition(scafold, sub_list, max_len):
    max_len = (max_len + 1) // 2
    inf = 10**9
    scafold = unravel(scafold)
    sub_list = list(map(unravel, sub_list))

    min_char = [inf for char in scafold]
    min_char.append(0) # dummy variable so that min_char[-1] = 0
    backtrack = [None for char in scafold]

    for i in range(len(scafold)):
        for sub_idx in range(len(sub_list)):
            len_sub = len(sub_list[sub_idx])
            if i-len_sub >= -1 and scafold[(i-len_sub+1) : i+1] == sub_list[sub_idx] and min_char[i-len_sub] + 1 < min_char[i]:
                min_char[i] = min_char[i-len_sub] + 1
                backtrack[i] = sub_idx


    reversed_partition = []
    cur_idx = len(scafold) - 1
    if min_char[cur_idx] == inf:  # no solution found
        return [], False

    while cur_idx != -1:
        sub_idx = backtrack[cur_idx]
        cur_idx = cur_idx - len(sub_list[sub_idx])
        reversed_partition.append(chr(ord("A") + sub_idx))

    if len(reversed_partition) > max_len:
        """
        print("scafold", scafold)
        print("sub_list", sub_list)
        print(list(reversed(reversed_partition)))
        """
        return [], False
    return list(reversed(reversed_partition)), True

def prefix_match(pattern, scafold):
    pat_len = len(pattern)
    if pat_len > len(scafold):
        return [], False

    for i in range(pat_len):
        if i < pat_len - 1:
            if pattern[i] != scafold[i]:
                return [], False
        elif pattern[i] == "L" or pattern[i] == "R":
            if pattern[i] != scafold[i]:
                return [], False
            return scafold[pat_len:], True
        else:
            if scafold[i] == "L" or scafold[i] == "R":
                return [], False
            if pattern[i] == scafold[i]:
                return scafold[pat_len:], True
            if pattern[i] > scafold[i]:
                return [], False
            return [scafold[i]-pattern[i]] + scafold[pat_len:], True

def get_len(prefix):
    count_char = 0
    for char in prefix:
        if char == "L" or char == "R":
            count_char += 1
        else:
            num = char
            while num > 0:
                num //= 10
                count_char += 1
    count_char += len(prefix) - 1  # commas
    return count_char

def get_prefixes(scafold, max_len):
    prefixes = []
    for i in range(len(scafold)):
        if get_len(scafold[0:i]) > max_len:
            break
        prefix = scafold[0:i+1]
        if prefix[-1] == "L" or prefix[-1] == "R":
            if get_len(prefix) <= max_len:
                prefixes.append(prefix)
        else:
            for ending in range(1, prefix[-1]+1):
                if get_len(prefix[0:-1] + [ending]) <= max_len:
                    prefixes.append(prefix[0:-1] + [ending])
    return prefixes


def get_partitions(scafold, patterns, max_len):
    if not scafold:
        return [patterns]

    return_splits = []
    for pattern in patterns:
        sliced_scafold, can_slice = prefix_match(pattern, scafold)
        if can_slice:
            for part in get_partitions(sliced_scafold, patterns, max_len):
                return_splits.append(part)

    if len(patterns) < 3:
        for pref in get_prefixes(scafold, max_len):
            sliced_scafold, can_slice = prefix_match(pref, scafold)
            if can_slice:
                for part in get_partitions(sliced_scafold, patterns + [pref], max_len):
                    return_splits.append(part)

    return return_splits

def find_partition(cur_map):
    max_len = 20
    scafold = get_path(cur_map)
    partition_list = get_partitions(scafold, [], max_len)
    scafold_str = ""
    """
    for char in scafold:
        scafold_str += str(char)
        scafold_str += ","
    print(scafold_str, len(scafold))
    print(partition_list)
    print(len(partition_list))
    """
    for part in partition_list:
        str_part, flag = partition(scafold, part, max_len)
        if flag:
            return part, str_part
    raise Exception("Noperino")

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

    memory = collections.defaultdict(int, memory_temp)
    if memory[0] != 1:
        raise RuntimeError("Assumption is wrong(memory[0] != 1)", memory[0])
    memory[0] = 2

    term_flag = False
    old_base = 0
    old_i = 0
    part, solution = find_partition(cur_map)
    print(solution)

    print_list(solution)
    for i in range(len(part)):
        print_list(part[i])
        print(part[i], get_len(part[i]))
    print_list(["n"]);

    while not term_flag:
        run_iter(memory)
        print(chr(output_reg), end="")

    dust = output_reg
    print("The amount of collected dust is", dust)



if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_program(memory)
    except Exception as exc:
        print(exc)