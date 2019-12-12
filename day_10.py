import copy
import functools

class node:
    vector = [0, 0]
    next = None
    last = None
    def __init__(self, vector, next = None, last = None):
        self.vector = vector
        self.next = next
        self.last = last

def cross_product(vector, other_vector):
    return (vector[0]*other_vector[1] - vector[1]*other_vector[0])

def in_upper_half(vector):
    return vector[0] > 0 or (vector[0] == 0 and vector[1] > 0)

def compare_vectors(vector, other_vector):
    if in_upper_half(other_vector) and not in_upper_half(vector):
        return -1
    if not in_upper_half(other_vector) and in_upper_half(vector):
        return 1
    return cross_product(vector, other_vector)

def find_first_node(first_node):
    cur_node = first_node.next
    initial_vector = [0, -1]
    while compare_vectors(cur_node.vector, initial_vector) <= 0:
        cur_node = cur_node.next
    return cur_node.last

if __name__ == "__main__":
    file = open("input.txt", "r")
    points = []
    y = 0
    for line in file:
        line = line.replace("\n", "")
        x = 0
        for symbol in line:
            if symbol == "#":
                points.append((x,y))
            x += 1
        y += 1

    max_seen_count = 0
    loc_x = 0
    loc_y = 0

    for point in points:
        vectors = []
        for point2 in points:
            if point2 != point:
                vectors.append([point2[0]-point[0], point2[1]-point[1]])

        cmp = functools.cmp_to_key(compare_vectors)
        vectors.sort(key=cmp)

        last_vector = None
        seen_count = 0
        for vector in vectors:
            if last_vector is None or compare_vectors(vector, last_vector) != 0:
                seen_count += 1
            last_vector = vector

        if seen_count > max_seen_count:
            max_seen_count = seen_count
            loc_x, loc_y = point

    print("Maximum number of objects able to be seen is", max_seen_count)
    print("It is at location",[loc_x, loc_y])

    vectors = []
    point = [loc_x, loc_y]
    for point2 in points:
        if point2 != point:
            vectors.append([point2[0] - point[0], point2[1] - point[1]])

    cmp = functools.cmp_to_key(compare_vectors)
    vectors.sort(key=cmp)

    first_node = node(None)
    first_node.next = node(vectors[0])
    first_node.next.last = first_node
    cur_node = first_node.next

    for vector in vectors[1:]:
        cur_node.next = node(vector)
        cur_node.next.last = cur_node
        cur_node = cur_node.next

    cur_node.next = first_node
    cur_node.next.last = cur_node
    num_asteroids = 200
    cur_node = find_first_node(first_node)
    last_vector = [0, 0]
    print("")

    for iter in range(num_asteroids-1):
        last_vector = cur_node.vector
        # remove node
        cur_node.next.last = cur_node.last
        cur_node.last.next = cur_node.next
        cur_node = cur_node.last

        while last_vector is not None and compare_vectors(cur_node.vector, last_vector) == 0:
            cur_node = cur_node.last
            if cur_node.vector == None:
                last_vector = None
                cur_node = cur_node.last

    last_y = cur_node.vector[1] + point[1]
    last_x = cur_node.vector[0] + point[0]
    print("The coordinates of the last removed point are", [last_x, last_y])
    print("The corresponding value is", last_x*100 + last_y)





