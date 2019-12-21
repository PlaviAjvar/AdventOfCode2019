import collections

'''
Assume 2 consecutive holes max.
Logic function which defines whether to jump:
y = v{9, 5, 3, 7, 11, 13}
Set bits(1) are assumed to be ground. Also the bit order goes from left to right.

Don't care combinations:
y = v{0, 1, 2, 4, 6, 8}

The MKNF is given as:
y = D(A'vB'vC')

The MKNF is better than the MDNF. Start with conjuction because T is zero at the start.

- 2 holes:

1) ###.. -> walk(forced)(12)

2) ##.#. -> walk(forced)(10)

3) ##..# -> jump(9)
##..#.. -> jump

4) #.#.# -> jump(forced)(5)
5) #..## -> jump(forced)(3)

- 1 hole:

1) #.### -> jump(forced)(7)

2) ##.## -> jump(11)
##.##.. -> jump

3) ###.# -> jump(13)
###.#..# -> jump

4) ####. -> walk(forced)(14)

- 0 holes:

1) ##### -> walk(always better)(15)
'''


'''
For part two we can and we need to realize a cascaded logic function(think MUX).
The rest is basically writing out all the cases on paper.
The only observation necessary is that:

A'X = (A'X)'' = (A v X')' 

This allows us to realize a cascade with two registers when negating. 
The cases are:

A' -> jump
AB'D -> jump
AB'D' -> walk
ABC'D' -> walk
ABC'DE'F' -> jump
ABC'DEF' -> jump
ABC'DEF -> jump
ABC'DE'FH' -> walk
ABC'DE'FG -> walk
ABC'DE'FG'HI -> jump
ABC'DE'FG'HI' -> jump
ABCD -> walk

In other words, jump can be written as(using a few reductions):
y = A' v AB'D v ABC'D(E'F)' v ABC'DE'FG'H =
= A' v AD(B' v BC'((E'F)' v G'H))


'''

def print_value(value):
    global output_queue
    output_queue.append(value)

def input_value():
    global input_queue
    empty_flag = (len(input_queue) > 1)
    return input_queue.popleft(), empty_flag

def print_list(values):
    global input_queue
    strr = ""
    for idx in range(len(values)):
        input_queue.append(ord(values[idx]))
        strr += values[idx]
    input_queue.append(ord("\n"))
    print(strr)

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

def run_program(memory_list):
    global old_base, old_i, term_flag, input_queue, output_queue
    size = len(memory_list)
    memory_temp = {i : memory_list[i] for i in range(size)}
    memory = collections.defaultdict(int, memory_temp)
    input_queue = collections.deque()
    output_queue = collections.deque()

    old_base = 0
    old_i = 0
    term_flag = False

    program_file = open("program_A.txt", "r")
    program = program_file.read()
    if program[-1] != "\n":
        program = program + "\n"
    print_list(program)

    print("***First part***\n")

    run_iter(memory)
    while output_queue:
        if output_queue[0] in range(0x110000):
            print(chr(output_queue.popleft()), end="")
        else:
            print(output_queue.popleft(), end="")

    print("\n\n")

    memory = collections.defaultdict(int, memory_temp)
    input_queue = collections.deque()
    output_queue = collections.deque()

    old_base = 0
    old_i = 0
    term_flag = False

    program_file = open("program_B.txt", "r")
    program = program_file.read()
    if program[-1] != "\n":
        program = program + "\n"
    print_list(program)

    print("\n\n***Second part***\n")

    run_iter(memory)
    while output_queue:
        if output_queue[0] in range(0x110000):
            print(chr(output_queue.popleft()), end="")
        else:
            print(output_queue.popleft(), end="")


if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_program(memory)
    except Exception as exc:
        print(exc)