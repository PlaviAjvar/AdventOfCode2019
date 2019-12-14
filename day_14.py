import collections

def get_left(left_side):
    left_side = left_side.replace(",", " ")
    reactant_str = left_side.split()
    reactants = []
    for i in range(0, len(reactant_str), 2):
        amount = int(reactant_str[i])
        id = reactant_str[i+1]
        reactants.append((id, amount))
    return reactants

def get_right(right_side):
    amount, id = right_side.split()
    amount = int(amount)
    return id, amount

def go_backwards(node, is_used, inv_reactions):
    is_used[node] = True
    for reactant in inv_reactions[node]:
        go_backwards(reactant[0])

def needed_ore(toposort, needed_fuel):
    start = "ORE"
    need = collections.defaultdict(int)
    need[destination] = needed_fuel

    for node in reversed(toposort):
        if node == start:
            break
        for reactant, amount in inv_reactions[node]:
            scaler = (need[node] // discrete_amount[node])
            if need[node] % discrete_amount[node] != 0:
                scaler += 1
            need[reactant] += scaler * amount

    return need[start]

if __name__ == "__main__":
    file = open("input.txt","r")
    graph = collections.defaultdict(list)
    in_degree = collections.defaultdict(int)
    inv_reactions = dict()
    discrete_amount = dict()
    arguments = []
    results = []
    max_amount = 0

    for line in file:
        left_side, right_side = line.split("=>")
        arguments.append(get_left(left_side))
        results.append(get_right(right_side))
        inv_reactions[results[-1][0]] = arguments[-1]
        discrete_amount[results[-1][0]] = results[-1][1]
        max_amount = max(max_amount, results[-1][1])

        for argument in arguments[-1]:
            graph[argument[0]].append(results[-1][0])
            in_degree[results[-1][0]] += 1
            max_amount = max(max_amount, argument[1])

    start = "ORE"
    destination = "FUEL"
    queue = collections.deque()
    queue.append(start)
    toposort = []

    while queue:
        node = queue.popleft()
        toposort.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    print("The minimal amount of necessary ore is", needed_ore(toposort, 1))

    have_ore = 10**12
    lower_bound, upper_bound = 0, have_ore

    while lower_bound != upper_bound:
        middle = (lower_bound + upper_bound) // 2  # amount of fuel
        need_ore = needed_ore(toposort, middle)
        if need_ore > have_ore:
            upper_bound = middle - 1
        else:
            lower_bound = middle

    print("The amount of fuel that can be produced from 1 trillion units of ore is", lower_bound)
