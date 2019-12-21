def highest_significant_bit(mask):
    order = 0
    while mask:
        order += 1
        mask >>= 1
    return order

def generate_masks(base_mask):
    highest_bit = highest_significant_bit(base_mask)
    for extra in range(1 << 3):
        yield (extra << highest_bit) | base_mask

def get_constituent(base_mask):
    if base_mask == 0:
        return 0, 0
    prefix_mask = (1 << 4) - 1
    if (base_mask & prefix_mask) == prefix_mask:
        return 0, 1
    jump_count = 0
    walk_count = 0

    for mask in generate_masks(base_mask):
        high_bit = highest_significant_bit(mask)

        if (mask & 1) != 0:
            state_reachable = [False] * 13
            state_reachable[0] = True
            state_reachable[1] = True
            for state in range(2, 13):
                if mask & (1 << state):
                    continue
                if state >= 4:
                    state_reachable[state] |= state_reachable[state - 4]
                state_reachable[state] |= state_reachable[state-1]
            if state_reachable[high_bit] or state_reachable[high_bit-1] or state_reachable[high_bit-2]:
                walk_count += 1

        if (mask & (1 << 3)) != 0:
            state_reachable = [False] * 13
            state_reachable[0] = True
            state_reachable[4] = True
            for state in range(5, 13):
                if mask & (1 << state):
                    continue
                if state >= 8:
                    state_reachable[state] |= state_reachable[state - 4]
                state_reachable[state] |= state_reachable[state - 1]
            if state_reachable[high_bit] or state_reachable[high_bit-1] or state_reachable[high_bit-2]:
                jump_count += 1

    if walk_count > jump_count:
        return 0, 1
    if walk_count < jump_count:
        return 1, 0
    return 0, 0



if __name__ == "__main__":
    prefix_mask = (1 << 4) - 1
    jump = [0] * (1 << 9)
    walk = [0] * (1 << 9)
    for mask in range(1 << 9):
        jump_can, walk_can = get_constituent(mask)
        jump[mask] |= jump_can
        walk[mask] |= walk_can

    dnf = []
    cnf = []
    dont_care = []

    for field in range(1 << 9):
        if jump[field] < walk[field]:
            cnf.append(field)
        elif jump[field] > walk[field]:
            dnf.append(field)
        else:
            dont_care.append(field)

    print("Disjunctive normal form:", dnf)
    print("Conjuctive normal form:", cnf)
    print("Don't care combinations:", dont_care)