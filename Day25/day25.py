SUBJECT_NUMBER = 7
DIVISOR = 20201227
CARD_PUB_KEY = 16616892
DOOR_PUB_KEY = 14505727


def part1():
    card_loop_size = get_loop_size(SUBJECT_NUMBER, CARD_PUB_KEY)
    encryption_key = transform(DOOR_PUB_KEY, card_loop_size)

    return encryption_key


def get_loop_size(subject_number, transformation_result):
    loops_done = 0
    result = 1
    while True:
        if result == transformation_result:
            return loops_done

        result = (result * subject_number) % DIVISOR
        loops_done += 1


def transform(subject_number, loops):
    result = 1
    for _ in range(loops):
        result = (result * subject_number) % DIVISOR

    return result


if __name__ == "__main__":
    print(part1())
