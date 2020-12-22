def part1():
    food_clues = read_food_list()

    possible_words = set()
    for allergen in food_clues:
        common_words = get_common_words(food_clues[allergen])
        for w in common_words:
            possible_words.add(w)

    ingredients = read_only_ingredients()
    impossible_word_freq = 0
    for food in ingredients:
        if food not in possible_words:
            impossible_word_freq += 1

    return impossible_word_freq


def get_common_words(sets):
    # Return words that appear in all of the given sets
    common_words = []
    for word in sets[0]:
        if all([word in sets[i] for i in range(1, len(sets))]):
            common_words.append(word)

    return common_words


def read_food_list():
    f = open("input.txt", "r")

    # clues is dictionary containing allergen-(list of sets of possible words)
    # pairs
    clues = {}
    for line in f.readlines():
        words, allergens = line.split(" (contains ")
        words = set(words.split())
        allergens = allergens[:-2].split(", ")

        for allergen in allergens:
            if not clues.get(allergen):
                clues[allergen] = [words]
            else:
                clues[allergen].append(words)

    f.close()
    return clues


def read_only_ingredients():
    f = open("input.txt", "r")

    ingredients = []
    for line in f.readlines():
        words, _ = line.split(" (contains ")
        ingredients += words.split()

    return ingredients


if __name__ == "__main__":
    print(part1())
