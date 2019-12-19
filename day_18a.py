import itertools
import collections

def find_start(triton_map):
    for row_idx in range(len(triton_map)):
        for col_idx in range(len(triton_map[0])):
            if triton_map[row_idx][col_idx] == "@":
                yield row_idx, col_idx

def bfs(triton_map, keys, idx_map):
    key_count = len(keys)
    row_count = len(triton_map)
    col_count = len(triton_map[0])
    inf = 10**9
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    visited = collections.defaultdict(bool)
    x_start, y_start = zip(*find_start(triton_map))
    queue = collections.deque()
    queue.append((x_start, y_start, 0, 0))
    last_distance = 0
    visited[(x_start, y_start, 0)] = True
    num_robots = len(x_start)

    while queue:
        cur_x, cur_y, cur_mask, cur_dist = queue.popleft()
        if cur_mask == (1 << key_count) - 1:
            return cur_dist

        if cur_dist > last_distance:
            print("Distance", last_distance, "clear.")
            last_distance = cur_dist

        for robot in range(num_robots):
            for direction in range(4):
                new_x, new_y = (cur_x[robot] + dx[direction], cur_y[robot] + dy[direction])
                if new_x >= row_count or new_x < 0 or new_y >= col_count or new_y < 0:
                    continue
                if triton_map[new_x][new_y] == "#":
                    continue
                if triton_map[new_x][new_y].isupper():
                    if cur_mask & (1 << idx_map[triton_map[new_x][new_y].lower()]) == 0:
                        continue

                new_bit = 0
                if triton_map[new_x][new_y].islower():
                    new_bit = (1 << idx_map[triton_map[new_x][new_y]])
                new_mask = cur_mask | new_bit

                arr_x = tuple(cur_x[x_idx] if x_idx != robot else new_x for x_idx in range(num_robots))
                arr_y = tuple(cur_y[y_idx] if y_idx != robot else new_y for y_idx in range(num_robots))

                if not visited[(arr_x, arr_y, new_mask)]:
                    visited[(arr_x, arr_y, new_mask)] = True
                    queue.append((arr_x, arr_y, new_mask, cur_dist + 1))


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

    print("First part\n")
    first_dist = bfs(triton_map, keys, idx_map)
    print("\n")

    print("The minimum distance to collect all keys is", first_dist, "\n")
