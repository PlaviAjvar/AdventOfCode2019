def run_iter(memory):
    size = len(memory)
    i = 0
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

            print("Input value:")
            memory[res_idx] = int(input())
            i += 2

        elif instr[4] == 4: # output
            if instr[2] == 0:
                value = memory[memory[i + 1]]
            else:
                value = memory[i + 1]
            print(value)
            i += 2

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
            break
        else:
            raise RuntimeError("Something went horribly wrong")

if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_iter(memory)
    except Exception as exc:
        print(exc)