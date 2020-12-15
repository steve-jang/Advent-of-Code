STARTING_NUMBERS = [16, 11, 15, 0, 1, 7]


def solution(n):
    # numbers_spoken contains number-occurence pairs, where occurence
    # is a list containing the turn numbers of up to 2 previous occurences
    # of number, with the last element being the most recent turn of occurence.
    numbers_spoken = {}

    for t in range(n):
        if t < 6:
            # Starting numbers
            current_number = STARTING_NUMBERS[t]
            numbers_spoken[current_number] = [t]
        else:
            occurences = numbers_spoken.get(current_number)
            if occurences:
                length = len(occurences)
                if length == 1:
                    current_number = 0
                elif length == 2:
                    current_number = occurences[1] - occurences[0]
                else:
                    raise Exception("invalid occurences len")

                store_number(numbers_spoken, current_number, t)
            else:
                raise Exception("numbers not stored properly")

    return current_number


def store_number(numbers_spoken, number, turn):
    if numbers_spoken.get(number):
        length = len(numbers_spoken[number])
        if length == 1:
            numbers_spoken[number].append(turn)
        elif length == 2:
            numbers_spoken[number] = [numbers_spoken[number][1], turn]
        else:
            raise Exception
    else:
        numbers_spoken[number] = [turn]


if __name__ == "__main__":
    # Part 1
    print(solution(2020))

    # Part 2
    print(solution(30000000))
