def part1():
    tickets = extract_tickets()
    rules = extract_rules()

    error_rate = 0
    for ticket in tickets:
        for n in ticket:
            satisfied = False
            for rule in rules:
                if rule[0] <= n <= rule[1]:
                    satisfied = True
                    break

            if not satisfied:
                error_rate += n

    return error_rate


def extract_tickets():
    # Returns a list of (list of numbers representing tickets)
    f = open("nearby.txt", "r")
    tickets = [[int(n) for n in line.split(",")] for line in f.readlines()]
    f.close()
    return tickets


def extract_rules():
    # Returns a list of (2-item lists representing each range)
    f = open("rules.txt", "r")
    rules = []
    for line in f.readlines():
        for word in line.split():
            if "-" in word:
                rules.append([int(n) for n in word.split("-")])

    f.close()
    return rules


def part2():
    rules = extract_rules()
    tickets = [t for t in extract_tickets() if is_ticket_valid(t, rules)]
    field_count = len(tickets[0])
    specific_rules = extract_specific_rules()
    field_order = {}

    # This populates field_order with (field index)-(list of satisfying fields) pairs
    for i in range(field_count):
        field_order[i] = []
        for field in specific_rules:
            values = [ticket[i] for ticket in tickets]
            field_match = True
            for value in values:
                if not is_rule_satisfied(specific_rules[field], value):
                    field_match = False
                    break

            if field_match:
                field_order[i].append(field)

    # This converts field_order into field-(matching index) pairs
    filtered_order = {}
    while field_order:
        for k in field_order:
            if len(field_order[k]) == 1:
                field = field_order.pop(k)[0]
                filtered_order[field] = k
                for j in field_order:
                    field_order[j].remove(field)

                break

    # This multiplies values of fields starting with "departure"
    my_ticket = [int(n) for n in open("my_ticket.txt", "r").readline().split(",")]
    result = 1
    for field in filtered_order:
        if "departure" in field:
            result *= my_ticket[filtered_order[field]]

    return result



def is_ticket_valid(ticket, rules):
    for n in ticket:
        valid_field = False
        for rule in rules:
            if rule[0] <= n <= rule[1]:
                valid_field = True
                break

        if not valid_field:
            return False

    return True


def is_rule_satisfied(rule, value):
    for interval in rule:
        if interval[0] <= value <= interval[1]:
            return True

    return False


def extract_specific_rules():
    f = open("rules.txt", "r")
    rules = {}

    for line in f.readlines():
        field, ranges = line.split(": ")
        rules[field] = []
        for word in ranges.split():
            if "-" in word:
                rules[field].append([int(n) for n in word.split("-")])

    f.close()
    return rules



if __name__ == "__main__":
    print(part1())
    print(part2())
