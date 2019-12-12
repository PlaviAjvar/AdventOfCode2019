import sys
import collections

def get_depth(node, pointer_up, visited, tree_depth):
    if node == None:
        return -1
    if visited[node]:
        return tree_depth[node]
    visited[node] = True
    tree_depth[node] = get_depth(pointer_up[node], pointer_up, visited, tree_depth) + 1
    return tree_depth[node]

def get_dist(start, destination, tree, visited):
    queue = collections.deque()
    distance = dict()
    for node in visited:
        distance[node] = len(visited) + 1

    visited[start] = True
    queue.append(start)
    distance[start] = 0

    while queue:
        top = queue.popleft()
        if top == destination:
            break
        for neighbor in tree[top]:
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True
                distance[neighbor] = distance[top] + 1

    return distance[destination] - 2


if __name__ == "__main__":
    sys.setrecursionlimit(10**6)
    file = open("input.txt", "r")
    pointer_up = dict()
    visited = dict()
    tree_depth = dict()
    tree = dict()

    for line in file:
        large_obj, orbiting_obj = line.split(")")
        orbiting_obj = orbiting_obj.replace("\n", "")

        pointer_up[orbiting_obj] = large_obj
        if not large_obj in pointer_up:
            pointer_up[large_obj] = None
        visited[orbiting_obj] = False
        visited[large_obj] = False

        if not large_obj in tree:
            tree[large_obj] = []
        tree[large_obj].append(orbiting_obj)

        if not orbiting_obj in tree:
            tree[orbiting_obj] = []
        tree[orbiting_obj].append(large_obj)


    total_depth = 0
    for node in pointer_up:
        total_depth += get_depth(node, pointer_up, visited, tree_depth)
    print("The total sum is", total_depth)

    for node in visited:
        visited[node] = False
    print("The distance to santa is", get_dist("YOU", "SAN", tree, visited))