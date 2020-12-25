CUPS = [7, 8, 9, 4, 6, 5, 1, 2, 3]


class Cup:
    def __init__(self, number, next_cup):
        self.number = number
        self.next = next_cup


def part1():
    # cups is a dict containing (cup number)-Cup pairs
    cups = store_cups(CUPS)

    first_cup = cups[CUPS[0]]
    for _ in range(100):
        first_cup = move_cups(first_cup, cups, 9)

    # Starting from the cup after cup 1, find next cups
    result = ""
    current_cup = cups[1].next
    for _ in range(8):
        result += str(current_cup.number)
        current_cup = current_cup.next

    return result


def store_cups(all_cups):
    prev_cup = None
    cups = {}
    for cup in all_cups:
        current_cup = Cup(cup, None)
        cups[cup] = current_cup
        if prev_cup:
            prev_cup.next = current_cup

        prev_cup = current_cup

    # Make last cup's next be the first cup to complete cycle
    first_cup = cups[all_cups[0]]
    last_cup = cups[all_cups[-1]]
    last_cup.next = first_cup

    return cups


def move_cups(first_cup, cups, max_cup):
    # Return the next first cup after doing one move.
    # Get the next three cups
    next1 = first_cup.next
    next2 = next1.next
    next3 = next2.next

    new_first_cup = next3.next

    invalid_targets = [first_cup.number, next1.number,
                       next2.number, next3.number]

    # Find destination cup
    target_number = first_cup.number - 1
    if target_number <= 0:
        target_number = max_cup

    while target_number in invalid_targets:
        if target_number == 1:
            target_number = max_cup
        else:
            target_number -= 1

    # Move the three cups after destination cup
    dest_cup = cups[target_number]
    dest_next = dest_cup.next
    dest_cup.next = next1
    next3.next = dest_next

    first_cup.next = new_first_cup
    return new_first_cup


def part2():
    cups_order = CUPS[:] + [i for i in range(10, 1000001)]
    cups = store_cups(cups_order)

    first_cup = cups[cups_order[0]]
    for i in range(10000000):
        first_cup = move_cups(first_cup, cups, 1000000)

    # Find the 2 cups after cup 1
    return cups[1].next.number * cups[1].next.next.number


if __name__ == "__main__":
    print(part1())
    print(part2())
