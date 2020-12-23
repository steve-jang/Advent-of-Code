def part1():
    player1_deck, player2_deck = get_decks()

    # Play until one player runs out of cards
    while player1_deck and player2_deck:
        player1_top_card = player1_deck.pop(0)
        player2_top_card = player2_deck.pop(0)

        if player1_top_card > player2_top_card:
            player1_deck += [player1_top_card, player2_top_card]
        elif player2_top_card > player1_top_card:
            player2_deck += [player2_top_card, player1_top_card]

    # Calculate score
    winning_deck = player1_deck if player1_deck else player2_deck
    winning_deck.reverse()
    score = 0
    for i, card in enumerate(winning_deck):
        score += (i + 1) * card

    return score


def get_decks():
    f = open("input.txt", "r")
    player1_deck = []
    player2_deck = []

    current_deck = player1_deck
    while True:
        line = f.readline()
        if not line:
            break

        line = line[:-1]
        if line.isnumeric():
            current_deck.append(int(line))
        elif "Player 2" in line:
            current_deck = player2_deck

    f.close()
    return player1_deck, player2_deck


def part2():
    player1_deck, player2_deck = get_decks()
    _, winning_deck = play_game(player1_deck, player2_deck)

    winning_deck.reverse()
    score = 0
    for i, card in enumerate(winning_deck):
        score += (i + 1) * card

    return score


def play_game(player1_deck, player2_deck):
    seen_configs = set()
    while True:
        if not player1_deck:
            return "Player 2", player2_deck
        if not player2_deck:
            return "Player 1", player1_deck

        current_config = (tuple(player1_deck), tuple(player2_deck))
        if current_config in seen_configs:
            # Infinite game prevention rule
            return "Player 1", player1_deck

        seen_configs.add(current_config)

        player1_card = player1_deck.pop(0)
        player2_card = player2_deck.pop(0)

        if (len(player1_deck) >= player1_card and
            len(player2_deck) >= player2_card):
            winner, _ = play_game(player1_deck[:player1_card],
                                  player2_deck[:player2_card])
            if winner == "Player 1":
                player1_deck += [player1_card, player2_card]
            else:
                player2_deck += [player2_card, player1_card]
        else:
            if player1_card > player2_card:
                player1_deck += [player1_card, player2_card]
            else:
                player2_deck += [player2_card, player1_card]


if __name__ == "__main__":
    print(part1())
    print(part2())
