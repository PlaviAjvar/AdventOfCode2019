def required_fuel(mass):
    fuel = max(mass//3 - 2, 0)
    total_fuel = fuel
    while fuel > 0:
        fuel = max(fuel//3 - 2, 0)
        total_fuel += fuel
    return total_fuel

if __name__ == "__main__":
    mass = []
    file = open("input.txt", "r")
    fuel = 0
    fuel_ception = 0

    for line in file:
        mass = int(line)
        fuel += max(mass//3 - 2, 0)
        fuel_ception += required_fuel(mass) #taking into account additional mass of fuel

    print("The necessary amount of fuel is", fuel)
    print("If taking into account additional mass of fuel it's", fuel_ception)