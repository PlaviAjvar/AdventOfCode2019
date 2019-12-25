import collections
import copy

'''
Doesn't work.
Dunno why.
'''

class intcode_computer:
    def input_value(self):
        if not self.input_queue:
            return -1
        return self.input_queue.popleft()

    def output_value(self, value):
        self.output_queue.append(value)

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
                if instr[2] == 0:
                    res_idx = self.memory[self.i+1]
                elif instr[2] == 2:
                    res_idx = self.relative_base + self.memory[self.i+1]
                else:
                    raise RuntimeError("Invalid mode for op 3(parameter 1 for result)")

                self.memory[res_idx] = self.input_value()
                self.i += 2
                self.output_flag = False
                return

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
                return

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

    def __init__(self, memory_list, network_address):
        size = len(memory_list)
        memory_temp = {i : memory_list[i] for i in range(size)}
        self.memory = collections.defaultdict(int, memory_temp)
        self.relative_base = 0
        self.i = 0
        self.input_queue = collections.deque()
        self.input_queue.append(network_address)
        self.output_queue = collections.deque()
        self.output_flag = False

def run_network(memory_list):
    num_computers = 50
    network = [intcode_computer(memory_list, computer) for computer in range(num_computers)]
    for computer in range(num_computers):
        network[computer].run_iter()
        network[computer].run_iter()

    while True:
        for computer in range(num_computers):
            network[computer].run_iter()
            if network[computer].output_flag:
                while len(network[computer].output_queue) % 3 != 0:
                    network[computer].run_iter()
                    
                address = network[computer].output_queue.popleft()
                x = network[computer].output_queue.popleft()
                y = network[computer].output_queue.popleft()

                if address == 255:
                    print("The y value of the first packet sent to address 255 is", y)
                    return

                network[address].input_queue.append(x)
                network[address].input_queue.append(y)

            elif network[computer].input_queue:
                network[computer].run_iter()


if __name__ == "__main__":
    file = open("input.txt","r")
    memory = list(map(int, file.read().split(",")))
    try:
        run_network(memory)
    except Exception as exc:
        print(exc)