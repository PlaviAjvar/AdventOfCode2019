import itertools
import collections

####
# DISCLAIMER
# This solution is wrong
####

# right solution for wrong problem
# well right if there were no bugs in the code(which there are)
# runs robots in parallel

def find_start(triton_map):
    for row_idx in range(len(triton_map)):
        for col_idx in range(len(triton_map)):
            if triton_map[row_idx][col_idx] == "@":
                yield row_idx, col_idx

def apply_mask(cur_x, cur_y, dir_mask, num_robots):
    dx = [1, 0, -1, 0, 0]
    dy = [0, 1, 0, -1, 0]
    new_x, new_y = [0] * num_robots, [0] * num_robots

    for cur_idx in range(num_robots):
        direction = dir_mask % 5
        dir_mask //= 5
        new_x[cur_idx] = cur_x[cur_idx] + dx[direction]
        new_y[cur_idx] = cur_y[cur_idx] + dy[direction]

    return tuple(new_x), tuple(new_y)

def get_valid_variations(triton_map, cur_x, cur_y, cur_mask, num_robots, row_count, col_count):
    dx = [1, 0, -1, 0, 0]
    dy = [0, 1, 0, -1, 0]
    list_variations = []

    def valid_util(rec_idx, cur_variation):
        if rec_idx == num_robots:
            list_variations.append(cur_variation)
            return

        for direction in range(5):
            new_x, new_y = (cur_x[rec_idx] + dx[direction]), (cur_y[rec_idx] + dy[direction])
            if new_x >= row_count or new_x < 0 or new_y >= col_count or new_y < 0:
                continue
            if triton_map[new_x][new_y] == "#":
                continue
            if triton_map[new_x][new_y].isupper():
                if cur_mask & (1 << idx_map[triton_map[new_x][new_y].lower()]) == 0:
                    continue
            valid_util(rec_idx + 1, cur_variation + direction * (5 ** rec_idx))

    valid_util(0, 0)
    return list_variations


def bfs(triton_map, keys, idx_map):
    key_count = len(keys)
    row_count = len(triton_map)
    col_count = len(triton_map[0])
    inf = 10**9

    visited = collections.defaultdict(bool)
    x_start, y_start = zip(*find_start(triton_map))
    num_robots = len(x_start)
    queue = collections.deque()
    queue.append((x_start, y_start, 0, 0))
    last_distance = 0
    visited[(x_start, y_start, 0)] = True

    while queue:
        cur_x, cur_y, cur_mask, cur_dist = queue.popleft()
        if cur_mask == (1 << key_count) - 1:
            return cur_dist

        if cur_dist > last_distance:
            print("Distance", last_distance, "clear.")
            last_distance = cur_dist

        valid_variations = get_valid_variations(triton_map, cur_x, cur_y, cur_mask, num_robots, row_count, col_count)

        for dir_mask in valid_variations:
            x_arr, y_arr = apply_mask(cur_x, cur_y, dir_mask, num_robots)

            new_mask = cur_mask
            for (new_x, new_y) in zip(x_arr, y_arr):
                if triton_map[new_x][new_y].islower():
                    new_bit = (1 << idx_map[triton_map[new_x][new_y]])
                    new_mask |= new_bit

            if not visited[(x_arr, y_arr, new_mask)]:
                visited[(x_arr, y_arr, new_mask)] = True
                queue.append((x_arr, y_arr, new_mask, cur_dist + 1))


    raise Exception("No path in graph which collects all points")

def convert_to_4_part(triton_map):
    x_st, y_st = zip(*find_start(triton_map))
    x_start, y_start = x_st[0], y_st[0]
    triton_map_2nd = []
    for row_idx in range(len(triton_map)):
        if abs(row_idx - x_start) > 1:
            triton_map_2nd.append(triton_map[row_idx])
        else:
            if row_idx != x_start:
                row = triton_map[row_idx][0 : y_start-1] + "@#@" + triton_map[row_idx][y_start+2 :]
            else:
                row = triton_map[row_idx][0 : y_start-1] + "###" + triton_map[row_idx][y_start+2 :]
            triton_map_2nd.append(row)
    return triton_map_2nd

if __name__ == "__main__":
    file = open("input.txt", "r")
    triton_map = file.read().split("\n")
    keys = list(itertools.chain(*[[field for field in row if field.islower()] for row in triton_map]))
    idx_map = {keys[key_idx] : key_idx for key_idx in range(len(keys))}
    #print("The minimum distance to collect all keys is", bfs(triton_map, keys, idx_map))
    #triton_map_2nd = convert_to_4_part(triton_map)
    triton_map_2nd = triton_map
    outf = open("output.txt","w+")
    for row in triton_map_2nd:
        outf.write(row + "\n")
    print("The minimum distance to collect all keys in 2nd map is", bfs(triton_map_2nd, keys, idx_map))