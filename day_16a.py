import copy

def apply_pattern(cum_sum, i, pattern_len, array_size):
    def sum_c(left_idx, right_idx):
        if right_idx >= array_size:
            right_idx = array_size - 1
        if left_idx >= array_size:
            left_idx = array_size - 1
        return cum_sum[right_idx] - cum_sum[left_idx]

    new_value = 0

    for j in range(0, array_size, pattern_len):
        new_value += sum_c(j + i - 1, j + 2 * i - 1)
        new_value -= sum_c(j + 3 * i - 1, j + 4 * i - 1)

    new_value = abs(new_value) % 10
    return new_value


def solve(array):
    num_iter = 100
    array_size = len(array)

    for iter in range(num_iter):
        cum_sum = copy.deepcopy(array)
        for i in range(1, array_size):
            cum_sum[i] += cum_sum[i-1]
        for i in range(1, array_size):
            pattern_len = i * 4
            array[i] = apply_pattern(cum_sum, i, pattern_len, array_size)

    char_array = list(map(str, array))
    return char_array

if __name__ == "__main__":
    file = open("input.txt","r")
    str_input = file.read()
    array = [int(char) for char in str_input]
    padded_array = [0] + array

    char_array = solve(padded_array)
    offset = 1
    print(''.join(char_array[offset:offset+8]))