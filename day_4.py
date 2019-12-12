def has_same_digit(n):
    dig = [False] * 10
    while n > 0:
        if dig[n % 10] == True:
            return True
        dig[n % 10] = True
        n //= 10
    return False

def is_increasing(n):
    cur_dig = 10
    while n > 0:
        if cur_dig < n % 10:
            return False
        cur_dig = n % 10
        n //= 10
    return True

def is_password(n):
    if not has_same_digit(n):
        return False
    if not is_increasing(n):
        return False
    return True

def exists_pair(n):
    cur_dig = 10
    rep_count = 1
    while n > 0:
        rem = n % 10
        if cur_dig == rem:
            rep_count += 1
        else:
            if rep_count == 2:
                return True
            rep_count = 1
            cur_dig = rem
        n //= 10
    if rep_count == 2:
        return True
    return False

def is_password_constr(n):
    if not is_increasing(n):
        return False
    if not exists_pair(n):
        return False
    return True


if __name__ == "__main__":
    lower_bound, upper_bound = list(map(int, input().split("-")))
    count = 0
    for n in range(lower_bound, upper_bound):
        if is_password(n):
            count += 1
    print("The number of different passwords is", count)

    count_constr = 0
    for n in range(lower_bound, upper_bound):
        if is_password_constr(n):
            count_constr += 1
    print("The number of passwords with additional constraint is", count_constr)