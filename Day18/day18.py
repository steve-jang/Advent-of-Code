def part1():
    f = open("input.txt", "r")
    lines = [line[:-1] for line in f.readlines()]
    f.close()

    result = 0
    for line in lines:
        result += evaluate_line(line)

    return result


def evaluate_line(line):
    # Remove spaces and evaluate parentheses first
    expression = "".join(line.split())
    simplified_expression = evaluate_parens(expression, evaluate_line)

    result = 0
    i = 0
    while i < len(simplified_expression):
        symbol = simplified_expression[i]

        if i == 0:
            next_number, digits = find_next_number(-1, simplified_expression)
            result += next_number
            i += digits
        elif symbol == "+":
            next_number, digits = find_next_number(i, simplified_expression)
            result += next_number
            i += digits + 1
        else:
            # symbol == "*"
            next_number, digits = find_next_number(i, simplified_expression)
            result *= next_number
            i += digits + 1

    return result


def find_next_number(index, expression):
    # Return the next number in the expression after the given index.
    # If index = -1, then the first number of the expression is returned.
    result = ""
    index += 1

    while True:
        if index < len(expression) and expression[index].isnumeric():
            result += expression[index]
        else:
            return int(result), len(result)

        index += 1


def evaluate_parens(expression, eval_function):
    # Convert expression into a simplified expression containing no parens.
    new_expression = ""
    i = 0

    while i < len(expression):
        symbol = expression[i]

        if symbol == "(":
            close_paren = find_close_paren(i, expression)

            # Evaluate parentheses as separate expressions
            new_expression += str(eval_function(expression[i + 1:close_paren]))
            i = close_paren
        elif symbol != ")":
            new_expression += symbol

        i += 1

    return new_expression


def find_close_paren(open_paren, expression):
    # Return the index of the closing parenthesis matching the open
    # parenthesis at index open_paren, in expression.
    opened = 0
    for i, symbol in enumerate(expression):
        if i < open_paren:
            continue

        if symbol == "(":
            opened += 1
        elif symbol == ")":
            opened -= 1

        if opened == 0:
            return i


def part2():
    f = open("input.txt", "r")
    lines = [line[:-1] for line in f.readlines()]
    f.close()

    result = 0
    for line in lines:
        result += evaluate_line_advanced(line)

    return result


def evaluate_line_advanced(line):
    expression = "".join(line.split())
    simplified_expression = evaluate_parens(expression, evaluate_line_advanced)

    result = 0
    i = 0
    while i < len(simplified_expression):
        symbol = simplified_expression[i]

        if i == 0:
            next_number, digits = find_next_number(-1, simplified_expression)
            result += next_number
            i += digits
        elif symbol == "+":
            next_number, digits = find_next_number(i, simplified_expression)
            result += next_number
            i += digits + 1
        else:
            # symbol == "*"
            # Evaluate rest of expression first, then multiply result, as
            # * has lowest precedence
            return result * evaluate_line_advanced(simplified_expression[i + 1:])

    return result


if __name__ == "__main__":
    print(part1())
    print(part2())
