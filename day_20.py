import collections

def portal_opening(pluto_map, row_idx, col_idx):
    drow = [1, 0, -1, 0]
    dcol = [0, 1, 0, -1]
    for distance_scaler in range(1,3):
        for direction in range(4):
            new_row = row_idx + drow[direction] * distance_scaler
            new_col = col_idx + dcol[direction] * distance_scaler
            if new_row < 0 or new_row >= len(pluto_map) or new_col < 0 or new_col >= len(pluto_map[0]):
                continue
            if pluto_map[new_row][new_col] == ".":
                return (new_row, new_col)

def write_to_help(visited, pluto_map):
    helpfile = open("help_out.txt","w+")

    for row_idx in range(len(visited)):
        for col_idx in range(len(visited[0])):
            el = visited[row_idx][col_idx]
            if pluto_map[row_idx][col_idx] == ".":
                if el:
                    helpfile.write("x")
                else:
                    helpfile.write(".")
            elif pluto_map[row_idx][col_idx] == "#":
                helpfile.write("#")
            else:
                helpfile.write(" ")
        helpfile.write("\n")

def min_distance(pluto_map, x_start, y_start, x_end, y_end, portal_position, portal_at_pos):
    row_count = len(pluto_map)
    col_count = len(pluto_map[0])
    queue = collections.deque()
    visited = [[False] * col_count for row in pluto_map]
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    visited[x_start][y_start] = True
    queue.append((x_start, y_start, 0))

    while queue:
        x_cur, y_cur, cur_dist = queue.popleft()
        if (x_cur, y_cur) == (x_end, y_end):
            return cur_dist
        for direction in range(4):
            x_new, y_new = (x_cur + dx[direction]), (y_cur + dy[direction])
            if x_new < 0 or x_new >= row_count or y_new < 0 or y_new >= col_count:
                continue
            if pluto_map[x_new][y_new] == "." and not visited[x_new][y_new]:
                visited[x_new][y_new] = True
                queue.append((x_new, y_new, cur_dist + 1))

        portal = portal_at_pos[x_cur][y_cur]
        if portal != "":
            for x_other, y_other in portal_position[portal]:
                if not visited[x_other][y_other]:
                    visited[x_other][y_other] = True
                    queue.append((x_other, y_other, cur_dist + 1))

    raise Exception("There is no path to ZZ.")

def is_outer(x, y, row_count, col_count):
    return (x <= 2 or x >= row_count - 3 or y <= 2 or y >= col_count - 3)

def min_distance_recursive(pluto_map, x_start, y_start, x_end, y_end, portal_position, portal_at_pos):
    row_count = len(pluto_map)
    col_count = len(pluto_map[0])
    queue = collections.deque()
    visited = collections.defaultdict(bool)
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    visited[(x_start, y_start, 0)] = True
    queue.append((x_start, y_start, 0, 0))

    while queue:
        x_cur, y_cur, cur_dist, cur_level = queue.popleft()
        if (x_cur, y_cur) == (x_end, y_end) and cur_level == 0:
            return cur_dist
        for direction in range(4):
            x_new, y_new = (x_cur + dx[direction]), (y_cur + dy[direction])
            if x_new < 0 or x_new >= row_count or y_new < 0 or y_new >= col_count:
                continue
            if pluto_map[x_new][y_new] == "." and not visited[(x_new, y_new, cur_level)]:
                visited[(x_new, y_new, cur_level)] = True
                queue.append((x_new, y_new, cur_dist + 1, cur_level))

        portal = portal_at_pos[x_cur][y_cur]
        if portal != "":
            for x_other, y_other in portal_position[portal]:
                if (x_other, y_other) == (x_cur, y_cur):
                    continue
                if is_outer(x_cur, y_cur, row_count, col_count):
                    level_shift = -1
                else:
                    level_shift = 1
                if cur_level + level_shift < 0:
                    continue
                if not visited[(x_other, y_other, cur_level + level_shift)]:
                    visited[(x_other, y_other, cur_level + level_shift)] = True
                    queue.append((x_other, y_other, cur_dist + 1, cur_level + level_shift))

    raise Exception("There is no path to ZZ.")

def avg_coordinate(row_idx, x_port):
    if abs(row_idx - x_port) == 2:
        return (row_idx + x_port) // 2
    return row_idx*2 - x_port

def get_next(row_idx, col_idx, x_port, y_port):
    return avg_coordinate(row_idx, x_port), avg_coordinate(col_idx, y_port)

if __name__ ==  "__main__":
    file = open("input.txt", "r")
    pluto_map = []
    width = 0
    for line in file:
        if line[-1] == "\n":
            pluto_map.append(line[:-1])
        else:
            pluto_map.append(line)
        width = max(width, len(pluto_map[-1]))

    for row_idx in range(len(pluto_map)):
        pluto_map[row_idx] += " " * (width - len(pluto_map[row_idx]))

    portal_position = collections.defaultdict(list)
    portal_at_pos = [["" for column in line] for line in pluto_map]

    for row_idx in range(len(pluto_map)):
        for col_idx in range(len(pluto_map[0])):
            if pluto_map[row_idx][col_idx].isalnum():
                x_port, y_port = portal_opening(pluto_map, row_idx, col_idx)
                row_next, col_next = get_next(row_idx, col_idx, x_port, y_port)
                #print(pluto_map[row_idx][col_idx], pluto_map[row_next][col_next], [row_next, col_next])
                str_pos = pluto_map[row_idx][col_idx] + pluto_map[row_next][col_next]
                if ord(str_pos[0]) > ord(str_pos[1]):
                    str_pos = str_pos[1] + str_pos[0]
                portal_position[str_pos].append((x_port, y_port))
                portal_at_pos[x_port][y_port] = str_pos

    x_start, y_start = portal_position["AA"][0]
    x_end, y_end = portal_position["ZZ"][0]
    print("The minimum distance from AA to ZZ is", min_distance(pluto_map, x_start, y_start, x_end, y_end,\
                                                                portal_position, portal_at_pos))

    print("The minimum distance in a recursive maze is", min_distance_recursive(pluto_map, x_start, y_start,\
                                                                x_end, y_end, portal_position, portal_at_pos))