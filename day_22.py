def power(base, exponent, modulo):
    if exponent == 0:
        return 1
    half_power = power(base, exponent // 2, modulo)
    if exponent % 2 == 0:
        return (half_power*half_power) % modulo
    return (half_power*half_power*base) % modulo

def mod_inv(num, modulo):
    return power(num, modulo - 2, modulo)

def apply_repeat(scaler, offset, num_cards, repeat):
    offset = (((power(scaler, repeat, num_cards) - 1) % num_cards) * mod_inv(scaler-1, num_cards) * offset) % num_cards
    scaler = power(scaler, repeat, num_cards)
    return scaler, offset

def apply_operations(num_cards, operations, repeat):
    scaler = 1
    offset = 0

    for line in operations:
        line = line.replace("\n", "")
        if line == "deal into new stack":
            scaler = (-scaler) % num_cards
            offset = (-offset - 1) % num_cards
        else:
            N = int(line.split()[-1])
            operation = " ".join(line.split()[:-1])
            if operation == "cut":
                offset = (offset - N) % num_cards
            elif operation == "deal with increment":
                offset = (offset * N) % num_cards
                scaler = (scaler * N) % num_cards
            else:
                raise Exception("Invalid operation")

    scaler, offset = apply_repeat(scaler, offset, num_cards, repeat)
    return scaler, offset

def get_position(card, scaler, offset, num_cards):
    return (scaler * card + offset) % num_cards

def invert_operation(scaler, offset, num_cards):
    offset = (-offset * mod_inv(scaler, num_cards)) % num_cards
    scaler = mod_inv(scaler, num_cards) % num_cards
    return scaler, offset

def get_card(position, num_cards):
    inv_scaler, inv_offset = invert_operation(scaler, offset, num_cards)
    return (inv_scaler * position + inv_offset) % num_cards

if __name__ == "__main__":
    input_file = open("input.txt","r")
    operations = [line for line in input_file]

    num_cards = 10007
    repeat = 1
    scaler, offset = apply_operations(num_cards, operations, repeat)
    print("The position of card 2019 is", get_position(2019, scaler, offset, num_cards))

    num_cards = 119315717514047  # prime number so modular inverse is easy
    repeat = 101741582076661
    scaler, offset = apply_operations(num_cards, operations, repeat)
    print("The card at position 2020 in the second shuffled deck is", get_card(2020, num_cards))