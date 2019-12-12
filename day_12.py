import copy

def iterate(xyz, v):
    # apply gravity
    for i in range(4):
        for j in range(i + 1, 4):
            for var in range(3):  # x,y,z
                if xyz[var][i] < xyz[var][j]:
                    v[var][i] += 1
                    v[var][j] -= 1
                elif xyz[var][i] > xyz[var][j]:
                    v[var][i] -= 1
                    v[var][j] += 1

    # apply velocity
    for i in range(4):
        for var in range(3):
            xyz[var][i] += v[var][i]

def is_same(xyz, xyz_init, v, v_init, var):
    for moon_idx in range(4):
        if xyz[var][moon_idx] != xyz_init[var][moon_idx]:
            return False
        if v[var][moon_idx] != v_init[var][moon_idx]:
            return False
    return True

def find_cycle(xyz_init, v_init, var):
    xyz = copy.deepcopy(xyz_init)
    v = copy.deepcopy(v_init)
    count_iter = 0
    while True:
        count_iter += 1
        iterate(xyz, v)
        if is_same(xyz, xyz_init, v, v_init, var):
            break
    return count_iter

def gcd(n, m):
    if m == 0:
        return n
    return gcd(m, n % m)

def lcm(n, m):
    return n * m // gcd(n, m)

if __name__ == "__main__":
    vx = [0] * 4
    vy = [0] * 4
    vz = [0] * 4
    v = [vx, vy, vz]
    v_initial = copy.deepcopy(v)

    x = [15, -5, 0, 5]
    y = [-2, -4, -6, 9]
    z = [-6, -11, 0, 6]
    xyz = [x, y, z]
    xyz_initial = copy.deepcopy(xyz)

    num_steps = 1000
    for iter in range(num_steps):
        iterate(xyz, v)

    energy_total = 0
    for moon_idx in range(4):
        kinetic = 0
        potential = 0
        for var in range(3):
            kinetic += abs(v[var][moon_idx])
            potential += abs(xyz[var][moon_idx])
        energy_total += kinetic * potential

    print("The total energy after", num_steps, "iterations is", energy_total)

    xyz = copy.deepcopy(xyz_initial)
    v = copy.deepcopy(v_initial)

    x_len = find_cycle(xyz, v, 0)
    print("Found length of x-cycle", x_len)
    y_len = find_cycle(xyz, v, 1)
    print("Found length of y-cycle", y_len)
    z_len = find_cycle(xyz, v, 2)
    print("Found length of z-cycle", z_len)

    cycle = lcm(x_len, lcm(y_len, z_len))
    print("The number of iterations until a repeated state is", cycle)


