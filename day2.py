import copy

def run_iter(memory):
    size = len(memory)
    i = 0
    while i < size:
        if memory[i] == 99:
            break
        elif memory[i] == 1:
            memory[memory[i + 3]] = memory[memory[i + 1]] + memory[memory[i + 2]]
        else:
            memory[memory[i + 3]] = memory[memory[i + 1]] * memory[memory[i + 2]]
        i += 4

def get_pair(memory_start, final_val):
    for noun in range(100):
        for verb in range(100):
            memory = copy.deepcopy(memory_start)
            memory[1] = noun
            memory[2] = verb
            run_iter(memory)
            if memory[0] == final_val:
                return noun, verb

if __name__ == "__main__":
    val_1 = 12
    val_2 = 2
    file = open("input.txt","r")
    memory_start = list(map(int, file.read().split(",")))
    memory = copy.deepcopy(memory_start)
    memory[1] = val_1
    memory[2] = val_2
    run_iter(memory)
    print("Value at zero is", memory[0])

    noun, verb = get_pair(memory_start, 19690720)
    print("The pair is", noun, verb)
    print("The answer to the problem is", 100*noun + verb)