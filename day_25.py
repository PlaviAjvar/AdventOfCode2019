import collections

'''
Hell naw I ain't coding this shit.
'''

class intcode_computer:
    def input_value(self):
        return self.input_queue.popleft()

    def output_value(self, value):
        print(chr(value), end="")
        self.output_queue.append(value)

    def input_command(self, command):
        for element in command:
            self.input_queue.append(element)

    def run_iter(self):
        while True:
            instr = [(self.memory[self.i] // 10**(4-k)) % 10 for k in range(5)]

            if instr[4] == 1 or instr[4] == 2: # add or multiply
                if instr[2] == 0:
                    left_val = self.memory[self.memory[self.i+1]]
                elif instr[2] == 2:
                    left_val = self.memory[self.relative_base + self.memory[self.i+1]]
                else:
                    left_val = self.memory[self.i+1]

                if instr[1] == 0:
                    right_val = self.memory[self.memory[self.i+2]]
                elif instr[1] == 2:
                    right_val = self.memory[self.relative_base + self.memory[self.i + 2]]
                else:
                    right_val = self.memory[self.i+2]

                if instr[0] == 0:
                    res_idx = self.memory[self.i+3]
                elif instr[0] == 2:
                    res_idx = self.relative_base + self.memory[self.i+3]
                else:
                    raise RuntimeError("Invalid mode for op 1/2(parameter 1 for result)")

                if instr[4] == 1:
                    self.memory[res_idx] = left_val + right_val
                else:
                    self.memory[res_idx] = left_val * right_val
                self.i += 4

            elif instr[4] == 3: # input
                if not self.input_flag and not self.input_queue:
                    self.input_flag = True
                    return
                else:
                    self.input_flag = False

                if instr[2] == 0:
                    res_idx = self.memory[self.i+1]
                elif instr[2] == 2:
                    res_idx = self.relative_base + self.memory[self.i+1]
                else:
                    raise RuntimeError("Invalid mode for op 3(parameter 1 for result)")

                self.memory[res_idx] = self.input_value()
                self.i += 2
                self.output_flag = False

            elif instr[4] == 4: # output
                if instr[2] == 0:
                    value = self.memory[self.memory[self.i + 1]]
                elif instr[2] == 2:
                    value = self.memory[self.relative_base + self.memory[self.i+1]]
                else:
                    value = self.memory[self.i + 1]

                self.output_value(value)
                self.i += 2
                self.output_flag = True

            elif instr[4] == 5 or instr[4] == 6: # jump if true/false
                if instr[2] == 0:
                    test_bit = self.memory[self.memory[self.i+1]]
                elif instr[2] == 2:
                    test_bit = self.memory[self.relative_base + self.memory[self.i+1]]
                else:
                    test_bit = self.memory[self.i + 1]

                jump_if_true = (instr[4] == 5)
                jump_if_false = not jump_if_true
                if (test_bit == 0 and jump_if_true) or (test_bit != 0 and jump_if_false):
                    self.i += 3
                    continue

                if instr[1] == 0:
                    jump_address = self.memory[self.memory[self.i+2]]
                elif instr[1] == 2:
                    jump_address = self.memory[self.relative_base + self.memory[self.i+2]]
                else:
                    jump_address = self.memory[self.i+2]

                self.i = jump_address

            elif instr[4] == 7 or instr[4] == 8: # less-than / equals
                if instr[2] == 0:
                    first_param = self.memory[self.memory[self.i+1]]
                elif instr[2] == 2:
                    first_param = self.memory[self.relative_base + self.memory[self.i+1]]
                else:
                    first_param = self.memory[self.i+1]

                if instr[1] == 0:
                    second_param = self.memory[self.memory[self.i+2]]
                elif instr[1] == 2:
                    second_param = self.memory[self.relative_base + self.memory[self.i+2]]
                else:
                    second_param = self.memory[self.i+2]

                if instr[0] == 0:
                    res_idx = self.memory[self.i+3]
                elif instr[0] == 2:
                    res_idx = self.memory[self.i+3] + self.relative_base
                else:
                    raise RuntimeError("Invalid mode for op 3(parameter 1 for result)")

                less_than_flag = (instr[4] == 7)
                if (less_than_flag and first_param < second_param) or (not less_than_flag and first_param == second_param):
                    self.memory[res_idx] = 1
                else:
                    self.memory[res_idx] = 0

                self.i += 4

            elif instr[4] == 9 and instr[3] == 0: # relative_base
                if instr[2] == 1:
                    self.relative_base += self.memory[self.i+1]
                elif instr[2] == 0:
                    self.relative_base += self.memory[self.memory[self.i+1]]
                else:
                    self.relative_base += self.memory[self.relative_base + self.memory[self.i+1]]
                self.i += 2

            elif instr[4] == 9 and instr[3] == 9:
                break
            else:
                raise RuntimeError("Something went horribly wrong")

    def __init__(self, memory_list):
        size = len(memory_list)
        memory_temp = {i : memory_list[i] for i in range(size)}
        self.memory = collections.defaultdict(int, memory_temp)
        self.relative_base = 0
        self.i = 0
        self.input_queue = collections.deque()
        self.output_queue = collections.deque()
        self.output_flag = False
        self.input_flag = False

def str_to_command(str):
    command = [ord(char) for char in str] + [ord("\n")]
    return command

def run_program(memory_list):
    computer = intcode_computer(memory_list)

    while True:
        computer.run_iter()
        command_str = input()
        command = str_to_command(command_str)
        computer.input_command(command)


if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_program(memory)
    except Exception as exc:
        print(exc)