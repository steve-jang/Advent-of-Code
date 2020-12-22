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


def part2():
    food_clues = read_food_list()

    possible_words = set()
    for allergen in food_clues:
        food_clues[allergen] = get_common_words(food_clues[allergen])

    # Match words to allergens until the solution is no longer updated
    matched_words = {}
    while True:
        outcome = match_words_to_allergens(matched_words, food_clues)
        if not outcome:
            break

    # Sort by allergen alphabetical order
    sorted_allergens = sorted(list(matched_words.keys()))

    # Generate canonical dangerous ingredient list
    result = ""
    for allergen in sorted_allergens:
        result += f"{matched_words[allergen]},"

    # Remove last trailing comma
    return result[:-1]


def match_words_to_allergens(matched_words, food_clues):
    # Populate matched_words with word-allergen pairs where word
    # matches the allergen. If none were matched, return False.
    updated = False
    for allergen in food_clues:
        if len(food_clues[allergen]) == 1:
            # Determine which words must match
            match = food_clues[allergen][0]
            matched_words[allergen] = match
            updated = True

            # Remove matched word from all other clues
            for allergen in food_clues:
                if match in food_clues[allergen]:
                    food_clues[allergen].remove(match)

    return updated


if __name__ == "__main__":
    print(part1())
    print(part2())
