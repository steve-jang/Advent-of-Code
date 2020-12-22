from day19 import read_rules, read_messages, satisfy_rule


def part2():
    rules = read_rules()
    messages = read_messages()

    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

    # Rule 0 is 8 11. Messages that satisfy rule 0 are ones which
    # satisfy rule 42 at least once, then satisfy rule 42 X times
    # then rule 31 X times, X >= 1.
    # In other words, messages that satisfy rule 0 are ones which satisfy
    # rule 42 X+Y times then rule 31 Y times, where X and Y >= 1

    valid_messages = 0
    for msg in messages:
        if is_rule0_satisfied(msg, rules):
            valid_messages += 1

    return valid_messages


def is_rule0_satisfied(msg, rules):
    # Figure out maximum number of times rule 42 can be satisfied
    max_satisfy_42 = 0
    rest_msg = msg
    while True:
        rest_msg = satisfy_rule(rest_msg, rules, 42)
        if rest_msg == False:
            break

        max_satisfy_42 += 1

    # As an example:
    # If max_satisfy_42 is 3, then try satisfying rule 31 one or two times
    # as this means we check if msg satisfies any of the sequences of rules
    # 42 42 42 31 31, 42 42 42 31, both allowed by rule 0
    for _ in range(max_satisfy_42):
        msg = satisfy_rule(msg, rules, 42)

    rest_msg = msg
    for i in range(1, max_satisfy_42):
        rest_msg = satisfy_rule(rest_msg, rules, 31)

        if rest_msg == "":
            return True
        elif rest_msg == False:
            return False

    return False


if __name__ == "__main__":
    print(part2())
