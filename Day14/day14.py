def part1():
    # Get components of each line of input
    f = open("input.txt", "r")
    lines = [l[:-1].split() for l in f.readlines()]

    # memory contains address-value pairs
    memory = {}

    current_mask = ""
    for keyword, _, arg in lines:
        # keyword is mask or mem[x], arg is the number after = of the line.
        if keyword == "mask":
            current_mask = arg
        else:
            # Convert given value to binary as a string
            bin_str_arg = bin(int(arg))[2:].zfill(36)
            result = ""
            for i, c in enumerate(current_mask):
                if c == "X":
                    result += bin_str_arg[i]
                else:
                    result += c

            result = int(result, 2)
            address = keyword[4:-1]
            memory[address] = result

    return sum(memory.values())


def part2():
    f = open("input.txt", "r")
    lines = [l[:-1].split() for l in f.readlines()]

    memory = {}
    current_mask = ""
    for keyword, _, arg in lines:
        if keyword == "mask":
            current_mask = arg
        else:
            address = int(keyword[4:-1])
            bin_str_address = bin(address)[2:].zfill(36)
            new_address = ""
            for i, c in enumerate(current_mask):
                if c == "0":
                    new_address += bin_str_address[i]
                else:
                    # If 1, then add 1, if X then add X
                    new_address += c

            value = int(arg)
            addresses = get_addresses(new_address)
            for a in addresses:
                memory[int(a, 2)] = value

    return sum(memory.values())


def get_addresses(float_address):
    result = [""]
    for c in float_address:
        new_result = []
        if c != "X":
            for a in result:
                new_result.append(a + c)
        else:
            for a in result:
                new_result.append(a + "1")
                new_result.append(a + "0")

        result = new_result

    return result


if __name__ == "__main__":
    print(part1())
    print(part2())
