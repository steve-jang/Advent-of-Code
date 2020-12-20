def solution(part):
    rules = read_rules()
    messages = read_messages()

    if part == 2:
        rules[8] = [[42], [42, 8]]
        rules[11] = [[42, 31], [42, 11, 31]]

    valid_messages = 0
    for msg in messages:
        if is_rule_satisfied(msg, rules, rule_number=0):
            valid_messages += 1

    return valid_messages


def read_rules():
    # Returns a dictionary of (rule number)-(list of rules) pairs.
    f = open("rules.txt", "r")
    rules = [line[:-1] for line in f.readlines()]
    f.close()

    result = {}
    for rule in rules:
        rule_number, sub_rules = rule.split(": ")
        rule_number = int(rule_number)
        result[rule_number] = []

        if "\"" in sub_rules:
            result[rule_number].append(sub_rules[1:-1])
        else:
            sub_rules = sub_rules.split(" | ")
            for sub_rule in sub_rules:
                result[rule_number].append([int(n) for n in sub_rule.split()])

    return result


def read_messages():
    # Returns a list of messages as strings.
    f = open("messages.txt", "r")
    messages = [line[:-1] for line in f.readlines()]

    f.close()
    return messages


def is_rule_satisfied(msg, rules, rule_number):
    # Rule is satisfied completely if after satisfying, there are no more
    # letters to check in the message.
    return satisfy_rule(msg, rules, rule_number) == ""


def satisfy_rule(msg, rules, rule_number):
    # Return the remaining part of the given message after satisfying
    # the given rule, or False if the rule cannot be satisfied.
    for sub_rule in rules[rule_number]:
        if type(sub_rule) == str:
            # Rules with characters
            if msg[:len(sub_rule)] == sub_rule:
                return msg[len(sub_rule):]
            else:
                return False
        else:
            # Rules with sub rule sequences
            rest_msg = satisfy_rule_sequence(msg, sub_rule, rules)
            if rest_msg != False:
                return rest_msg

    return False


def satisfy_rule_sequence(msg, rule_seq, rules):
    # Return the remaining part of the given message after satisfying
    # the given sequence of rules, or False if the rule cannot be satisfied.
    if not rule_seq:
        # Base case
        return msg

    for rule_number in rule_seq:
        rest_msg = satisfy_rule(msg, rules, rule_number)
        if rest_msg is False:
            return False
        else:
            return satisfy_rule_sequence(rest_msg, rule_seq[1:], rules)


if __name__ == "__main__":
    print(solution(part=1))
    print(solution(part=2))
