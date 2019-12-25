def mask_to_grid(mask, grid_size):
    grid = [[0] * grid_size for _ in range(grid_size)]
    for row_idx in range(grid_size):
        for col_idx in range(grid_size):
            grid[row_idx][col_idx] = (mask & 1)
            mask >>= 1
    return grid

def simulate(grid, grid_size):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    new_grid = [[0] * grid_size for _ in range(grid_size)]

    for row_idx, row in enumerate(grid):
        for col_idx, field in enumerate(row):
            count_adj = 0
            for direction in range(4):
                new_row, new_col = (row_idx + dx[direction]), (col_idx + dy[direction])
                if new_row < 0 or new_row >= grid_size or new_col < 0 or new_col >= grid_size:
                    continue
                if grid[new_row][new_col] == 1:
                    count_adj += 1

            if field == 1:
                new_grid[row_idx][col_idx] = 1 if count_adj == 1 else 0
            else:
                new_grid[row_idx][col_idx] = 1 if (count_adj == 2 or count_adj == 1) else 0

    return new_grid

def grid_to_mask(grid, grid_size):
    mask = 0
    shift = 1
    for row in grid:
        mask += shift * sum([row[idx] * (1 << idx) for idx in range(grid_size)])
        shift *= (1 << grid_size)
    return mask

def get_new_mask(mask, grid_size):
    grid = mask_to_grid(mask, grid_size)
    new_grid = simulate(grid, grid_size)
    new_mask = grid_to_mask(new_grid, grid_size)
    return new_mask

if __name__ == "__main__":
    file = open("input.txt","r")
    grid_size = 5
    grid = [[0] * grid_size for _ in range(grid_size)]
    for row_idx, line in enumerate(file):
        if line[-1] == "\n":
            line = line[:-1]
        grid[row_idx] = [1 if char == "#" else 0 for char in line]

    mask = grid_to_mask(grid, grid_size)
    processed_masks = set()
    processed_masks.add(mask)

    while True:
        mask = get_new_mask(mask, grid_size)
        if mask in processed_masks:
            print("The biodiversity rating for the first repeated layout is", mask)
            print("The grid corresponding to the given layout is:")
            for line in mask_to_grid(mask, grid_size):
                str_line = ["#" if field == 1 else "." for field in line]
                print("".join(str_line))
            break
        processed_masks.add(mask)