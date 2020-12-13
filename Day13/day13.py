def part1():
    f = open("input.txt", "r")
    lines = f.readlines()
    f.close()
    time = int(lines[0])
    buses = [int(bus) for bus in lines[1].split(",") if bus != "x"]

    bus_times = {}
    for b in buses:
        bus_times[b] = b - (time % b)

    for b in bus_times:
        if bus_times[b] == min(bus_times.values()):
            return b * bus_times[b]


def part2():
    f = open("input.txt", "r")
    lines = f.readlines()
    f.close()
    time = int(lines[0])

    # bus_offsets is a list of bus-offset pairs.
    bus_offsets = []
    for i, b in enumerate(lines[1].split(",")):
        if b != "x":
            bus_offsets.append((int(b), i % int(b)))

    # need to solve an equation of the form:
    # t = p1a1 - b1 = p2a2 - b2 = p3a3 - b3 = ...
    # Solve the above equation by solving the first two, then solving
    # the solution equation with subsequent equations.
    # let current equation be of the form t = eqn_p*a - eqn_b,
    # keeping track of only p and b.
    for i, bus in enumerate(bus_offsets):
        if i == 0:
            # Initially set variables
            eqn_p = bus[0]
            eqn_b = bus[1]
        else:
            p = bus[0]
            b = bus[1]

            # Update current equation being solved
            # Formula for the solution for t after the ith equation
            # (Manually worked out formula)
            eqn_b = -p * (((b - eqn_b) * modinv(p, eqn_p)) % eqn_p) + b
            eqn_p *= p

    return -eqn_b


# Functions for modinv (modular inverse) obtained from SO:
# https://stackoverflow.com/questions/16044553/solving-a-modular-equation-python
# Iterative Algorithm (xgcd)
def iterative_egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q # use x//y for floor "floor division"
        b, a, x, y, u, v = a, r, u, v, m, n

    return b, x, y


def modinv(a, m):
    g, x, y = iterative_egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m


if __name__ == "__main__":
    print(part1())
    print(part2())
