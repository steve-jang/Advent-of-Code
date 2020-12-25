BLACK = 1
WHITE = 2


def part1():
    tile_positions = get_tile_positions()
    tiles = setup_tiles(tile_positions)

    return black_tile_count(tiles)


def black_tile_count(tiles):
    count = 0
    for pos in tiles:
        if tiles[pos] == BLACK:
            count += 1

    return count


def setup_tiles(tile_positions):
    tiles = {(0, 0): WHITE}

    for tile_pos in tile_positions:
        if tiles.get(tile_pos):
            if tiles[tile_pos] == WHITE:
                tiles[tile_pos] = BLACK
            else:
                tiles[tile_pos] = WHITE
        else:
            tiles[tile_pos] = BLACK

    return tiles


def get_tile_positions():
    f = open("input.txt", "r")
    lines = [line[:-1] for line in f.readlines()]
    f.close()

    tiles = []
    for line in lines:
        current_tile = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == "n" or c == "s":
                current_tile.append(c + line[i + 1])
                i += 2
            else:
                current_tile.append(c)
                i += 1

        current_tile = simplify_tile(current_tile)
        tiles.append(current_tile)

    return tiles


def simplify_tile(tile_pos):
    # Remove redundant directions (e.g. nw then se), and change all
    # directions to be one of e, s, ne, and sw. Use a skewed-axis
    # coordinate system to represent the tile position, where the
    # positive x axis is the e direction, and the positive y axis is
    # the ne direction. Return the coordinate.
    direction_freq = {pos: 0 for pos in ["nw", "ne", "sw", "se", "w", "e"]}

    # First change all nw to w ne, and all se to e sw.
    for direction in tile_pos:
        if direction == "nw":
            direction_freq["w"] += 1
            direction_freq["ne"] += 1
        elif direction == "se":
            direction_freq["e"] += 1
            direction_freq["sw"] += 1
        else:
            direction_freq[direction] += 1

    east_dir = direction_freq["e"] - direction_freq["w"]
    ne_dir = direction_freq["ne"] - direction_freq["sw"]
    return east_dir, ne_dir


def part2():
    tile_positions = get_tile_positions()
    tiles = setup_tiles(tile_positions)
    tiles = track_adj_blacks(tiles)

    for i in range(100):
        tiles = update_tiles(tiles)

    return black_tile_count(tiles)


def track_adj_blacks(tiles):
    new_tiles = {}
    for coords in tiles:
        if tiles[coords] == BLACK:
            neighbours = get_neighbours(coords)
            for pos in neighbours:
                if not tiles.get(pos):
                    new_tiles[pos] = WHITE
                else:
                    new_tiles[pos] = tiles[pos]

            new_tiles[coords] = BLACK

    return new_tiles


def get_neighbours(coords):
    result = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != j:
                result.append((coords[0] + i, coords[1] + j))

    return result


def update_tiles(tiles):
    new_tiles = {}
    for coords in tiles:
        # Find only the new black tiles
        adj_blacks = adj_black_count(coords, tiles)
        if tiles[coords] == BLACK and not (adj_blacks == 0 or adj_blacks > 2):
            new_tiles[coords] = BLACK
        elif tiles[coords] == WHITE and adj_blacks == 2:
            new_tiles[coords] = BLACK

    new_tiles = track_adj_blacks(new_tiles)
    return new_tiles


def adj_black_count(coords, tiles):
    count = 0
    for coords in get_neighbours(coords):
        if tiles.get(coords) and tiles[coords] == BLACK:
            count += 1

    return count


if __name__ == "__main__":
    print(part1())
    print(part2())
