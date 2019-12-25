import collections

def count_col(grid, col_idx):
    count = 0
    for row in grid:
        count += row[col_idx]
    return count

def simulate(low_grid, grid, high_grid, grid_size):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    new_grid = [[0] * grid_size for _ in range(grid_size)]
    middle = (grid_size // 2, grid_size // 2)

    for row_idx, row in enumerate(grid):
        for col_idx, field in enumerate(row):
            if (row_idx, col_idx) == middle:
                continue
            count_adj = 0
            for direction in range(4):
                new_row, new_col = (row_idx + dx[direction]), (col_idx + dy[direction])

                if new_row < 0:
                    if high_grid[grid_size // 2 - 1][grid_size // 2]:
                        count_adj += 1
                elif new_row >= grid_size:
                    if high_grid[grid_size // 2 + 1][grid_size // 2]:
                        count_adj += 1
                elif new_col < 0:
                    if high_grid[grid_size // 2][grid_size // 2 - 1]:
                        count_adj += 1
                elif new_col >= grid_size:
                    if high_grid[grid_size // 2][grid_size // 2 + 1]:
                        count_adj += 1

                elif (new_row, new_col) != middle:
                    if grid[new_row][new_col] == 1:
                        count_adj += 1

                else:
                    if row_idx > middle[0]:
                        count_adj += sum(low_grid[-1])
                    elif row_idx < middle[0]:
                        count_adj += sum(low_grid[0])
                    elif col_idx > middle[0]:
                        count_adj += count_col(low_grid, grid_size-1)
                    else:
                        count_adj += count_col(low_grid, 0)

            if field == 1:
                new_grid[row_idx][col_idx] = 1 if count_adj == 1 else 0
            else:
                new_grid[row_idx][col_idx] = 1 if (count_adj == 2 or count_adj == 1) else 0

    return new_grid

def help_output(out_file, iteration, grids):
    out_file.write("Iteration " + str(iteration) + "\n\n")
    for grid in grids:
        out_file.write(str(grid))
        out_file.write("\n\n")
        for row in grids[grid]:
            out_file.write("".join(["#" if field == 1 else "." for field in row]) + "\n")
        out_file.write("\n")

if __name__ == "__main__":
    file = open("input.txt","r")
    grid_size = 5
    grid = [[0] * grid_size for _ in range(grid_size)]
    for row_idx, line in enumerate(file):
        if line[-1] == "\n":
            line = line[:-1]
        grid[row_idx] = [1 if char == "#" else 0 for char in line]

    grids = collections.defaultdict(lambda grid_size = grid_size : [[0] * grid_size for _ in range(grid_size)])
    grids[0] = grid
    num_iter = 200
    out_file = open("output.txt","w+")

    for iteration in range(num_iter):
        print("Iteration", iteration, "clear.")
        new_grids = collections.defaultdict(lambda grid_size = grid_size : [[0] * grid_size for _ in range(grid_size)])
        for level in range(-iteration-1, iteration+2):
            new_grids[level] = simulate(grids[level-1], grids[level], grids[level+1], grid_size)
        grids = new_grids

    count_bugs = 0
    for level in range(-num_iter, num_iter+1):
        count_bugs += sum([row.count(1) for row in grids[level]])
    print("The total number of bugs after", num_iter, "days in the recursive grid is", count_bugs)