import itertools
import copy

call_idx = 0
input_queue = []
cur_value = 0
start_iter = [0, 0, 0, 0, 0]
term_flag = False

def input_value():
    global call_idx
    global input_queue
    call_idx += 1
    # print(call_idx-1, input_queue)
    return input_queue[call_idx - 1]

def print_value(value):
    global cur_value
    # print("print", value)
    cur_value = value

def run_iter(memory, amp_idx):
    global start_iter
    global term_flag
    size = len(memory)
    i = start_iter[amp_idx]
    while i < size:
        instr = [(memory[i] // 10**(4-k)) % 10 for k in range(5)]
        #print(instr)

        if instr[4] == 1 or instr[4] == 2: # add or multiply
            if instr[2] == 0:
                left_val = memory[memory[i+1]]
            else:
                left_val = memory[i+1]

            if instr[1] == 0:
                right_val = memory[memory[i+2]]
            else:
                right_val = memory[i+2]

            if instr[0] == 0:
                res_idx = memory[i+3]
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
            else:
                raise RuntimeError("Invalid mode for op 3(parameter 1 for result)")

            memory[res_idx] = int(input_value())
            i += 2

        elif instr[4] == 4: # output
            if instr[2] == 0:
                value = memory[memory[i + 1]]
            else:
                value = memory[i + 1]
            print_value(value)
            i += 2
            start_iter[amp_idx] = i
            break


        elif instr[4] == 5 or instr[4] == 6: # jump if true/false
            if instr[2] == 0:
                test_bit = memory[memory[i+1]]
            else:
                test_bit = memory[i + 1]

            jump_if_true = (instr[4] == 5)
            jump_if_false = not jump_if_true
            if (test_bit == 0 and jump_if_true) or (test_bit != 0 and jump_if_false):
                i += 3
                continue

            if instr[1] == 0:
                jump_address = memory[memory[i+2]]
            else:
                jump_address = memory[i+2]

            i = jump_address

        elif instr[4] == 7 or instr[4] == 8: # less-than / equals
            if instr[2] == 0:
                first_param = memory[memory[i+1]]
            else:
                first_param = memory[i+1]

            if instr[1] == 0:
                second_param = memory[memory[i+2]]
            else:
                second_param = memory[i+2]

            if instr[0] == 0:
                res_idx = memory[i+3]
            else:
                raise RuntimeError("Invalid mode for op 3(parameter 1 for result)")

            less_than_flag = (instr[4] == 7)
            if (less_than_flag and first_param < second_param) or (not less_than_flag and first_param == second_param):
                memory[res_idx] = 1
            else:
                memory[res_idx] = 0

            i += 4

        elif instr[4] == 9 and instr[3] == 9:
            term_flag = True
            break
        else:
            raise RuntimeError("Something went horribly wrong")

def run_processor(memory, permutation):
    global input_queue
    global call_idx
    global cur_value
    global term_flag
    global start_iter
    term_flag = False
    start_iter = [0,0,0,0,0]
    amp_input = 0
    memories = [copy.deepcopy(memory) for i in range(5)]

    for amp_idx in range(5):
        input_queue = [permutation[amp_idx], amp_input]
        call_idx = 0
        run_iter(memories[amp_idx], amp_idx)
        amp_input = cur_value

    output_e = cur_value
    cyc_count = 0

    while not term_flag:
        input_queue = [amp_input]
        call_idx = 0
        run_iter(memories[cyc_count], cyc_count)
        cyc_count += 1
        if cyc_count >= 5:
            cyc_count = 0
            output_e = cur_value
        if amp_input == cur_value:
            break
        amp_input = cur_value

    return output_e


if __name__ == "__main__":
    file = open("input.txt", "r")
    memory_initial = list(map(int, file.read().split(",")))
    max_out = 0
    for permutation in itertools.permutations([5,6,7,8,9]):
        memory = copy.deepcopy(memory_initial)
        if max_out != None:
            max_out = max(max_out, run_processor(memory, permutation))
        else:
            max_out = run_processor(memory, permutation)
    print("The maximum value is", max_out)