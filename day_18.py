import itertools
import collections
import heapq

def find_start(triton_map):
    for row_idx in range(len(triton_map)):
        for col_idx in range(len(triton_map[0])):
            if triton_map[row_idx][col_idx] == "@":
                yield row_idx, col_idx

def find_keys(triton_map):
    for row_idx in range(len(triton_map)):
        for col_idx in range(len(triton_map[0])):
            if triton_map[row_idx][col_idx].islower():
                yield row_idx, col_idx


def find_distance(triton_map, x_start, y_start, x_end, y_end, mask):
    row_count = len(triton_map)
    col_count = len(triton_map[0])
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    inf = 10**9
    queue = collections.deque()
    queue.append((x_start, y_start, 0))
    visited = [[False for j in range(col_count)] for i in range(row_count)]

    while queue:
        cur_x, cur_y, cur_dist = queue.popleft()
        if (x_end, y_end) == (cur_x, cur_y):
            return cur_dist

        for direction in range(4):
            new_x, new_y = (cur_x + dx[direction], cur_y + dy[direction])
            if new_x >= row_count or new_x < 0 or new_y >= col_count or new_y < 0:
                continue
            if triton_map[new_x][new_y] == "#":
                continue
            if triton_map[new_x][new_y].isupper():
                if mask & (1 << idx_map[triton_map[new_x][new_y].lower()]) == 0:
                    continue

            if not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append((new_x, new_y, cur_dist + 1))

    return inf

def min_distance(triton_map, keys, idx_map):
    key_count = len(keys)
    inf = 10**9
    x_key, y_key = zip(*find_keys(triton_map))
    x_start, y_start = zip(*find_start(triton_map))

    x_key += x_start
    y_key += y_start
    for st_idx in range(len(x_start)):
        idx_map[(x_start[st_idx], y_start[st_idx])] = key_count + st_idx

    num_robots = len(x_start)
    priority_queue = []
    last_distance = 0
    heapq.heappush(priority_queue, (0, 0, tuple(range(key_count,key_count + num_robots))))
    distance = collections.defaultdict(lambda : inf)

    while priority_queue:
        cur_dist, cur_mask, key_list = heapq.heappop(priority_queue)
        cur_x = tuple(x_key[key] for key in key_list)
        cur_y = tuple(y_key[key] for key in key_list)
        if cur_mask == (1 << key_count) - 1:
            return cur_dist

        if cur_dist > last_distance:
            print("Distance", last_distance, "clear.")
            last_distance = cur_dist

        for robot in range(num_robots):
            for key in range(key_count):
                if cur_mask & (1 << key) != 0:
                    continue
                new_x, new_y = x_key[key], y_key[key]
                new_mask = cur_mask | (1 << key)
                new_dist = cur_dist + find_distance(triton_map, cur_x[robot], cur_y[robot], new_x, new_y, cur_mask)
                new_keylist = tuple(key_list[key_idx] if robot != key_idx else key for key_idx in range(num_robots))

                if new_dist < distance[(new_keylist, new_mask)]:
                    distance[(new_keylist, new_mask)] = new_dist
                    heapq.heappush(priority_queue, (new_dist, new_mask, new_keylist))

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

    print("Second part\n")
    triton_map_2nd = convert_to_4_part(triton_map)
    second_dist = min_distance(triton_map_2nd, keys, idx_map)
    print("\n")
    print("The minimum distance to collect all keys in 2nd map is", second_dist)

