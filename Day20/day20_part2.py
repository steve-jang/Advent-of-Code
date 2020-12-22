from day20 import Tile, get_tiles, get_match_data, TOP, BOTTOM, LEFT, RIGHT


def part2():
    tiles = get_tiles()
    top_left = arrange_tiles(tiles)
    ocean = get_ocean_map(top_left)
    monster = ["                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   "]

    # Rotate ocean map to find sea monsters
    monster_coords = rotate_ocean_for_monsters(ocean, monster)
    if not monster_coords:
        # If no monsters found flip the ocean and try again
        flip_vertical(ocean)
        monster_coords = rotate_ocean_for_monsters(ocean, monster)

    # Unoccupied coordinates is the number of "#" in ocean minus the
    # occupied coordinates
    return sum([row.count("#") for row in ocean]) - len(monster_coords)


def rotate_ocean_for_monsters(ocean, monster):
    monster_width = len(monster[0])
    monster_height = len(monster)

    ocean_height = len(ocean)
    ocean_width = len(ocean[0])

    # Rotate the given ocean to find sea monsters, if any monsters are found
    # return the coordinates occupied by the monsters.
    for _ in range(4):
        monster_coords = set()
        for x in range(ocean_height - monster_height + 1):
            for y in range(ocean_width - monster_width + 1):
                occupied_coords = find_monster_coords(ocean, monster, x, y)
                for coord in occupied_coords:
                    monster_coords.add(coord)

        if monster_coords:
            return monster_coords

        ocean = rotate_right(ocean)


def flip_vertical(pattern):
    # Assume pattern is square
    size = len(pattern)
    for i in range(size // 2):
        temp_row = pattern[i]
        pattern[i] = pattern[size - i - 1]
        pattern[size - i - 1] = temp_row


def rotate_right(pattern):
    new_pattern = []
    for i in range(len(pattern)):
        new_row = []
        for row in pattern:
            new_row.append(row[i])

        new_pattern.append("".join(reversed(new_row)))

    return new_pattern


def find_monster_coords(ocean, monster, x, y):
    # Return a set of all coordinates occupied by any monster found
    # in the given ocean with top left coordinate (x, y).
    occupied = set()
    for i, row in enumerate(monster):
        for j, c in enumerate(row):
            if c == "#":
                if ocean[x + i][y + j] != "#":
                    return set()
                else:
                    occupied.add((x + i, y + j))

    return occupied


def arrange_tiles(tiles):
    # Set adjacency info for all tiles. Also return the top left tile
    # after arranging, so that the arranged tiles can be traversed.
    todo = [list(tiles.values())[0]]
    tiles_seen = set()

    # For each tile set its adjacency data, and get the top left tile
    while todo:
        tile = todo.pop(-1)
        if tile.tile_id in tiles_seen:
            continue

        matches = get_match_data(tile, tiles)

        # Top left tile has no matching tile on top nor on the left
        if not (matches.get(TOP) or matches.get(LEFT)):
            top_left_tile = tile

        opp = {TOP: BOTTOM, BOTTOM: TOP, LEFT: RIGHT, RIGHT: LEFT}

        for pos in opp:
            pos_tile = matches.get(pos)
            if pos_tile:
                tile.adj_tiles[pos] = pos_tile
                pos_tile.adj_tiles[opp[pos]] = tile
                todo.append(pos_tile)

        tiles_seen.add(tile.tile_id)

    return top_left_tile


def get_ocean_map(top_left_tile):
    # Join arranged tiles together, without each tile's boundaries
    n_rows = 8 * 12
    ocean = ["" for _ in range(n_rows)]
    current_row_tile = top_left_tile
    current_tile = top_left_tile
    current_row = 0
    while current_row_tile:
        while current_tile:
            current_tile.pattern = current_tile.pattern[1:-1]
            for n, row in enumerate(current_tile.pattern):
                current_tile.pattern[n] = row[1:-1]

            for i, row in enumerate(current_tile.pattern):
                ocean[current_row + i] += current_tile.pattern[i]

            current_tile = current_tile.adj_tiles[RIGHT]

        current_row_tile = current_row_tile.adj_tiles[BOTTOM]
        current_tile = current_row_tile
        current_row += 8

    return ocean


if __name__ == "__main__":
    print(part2())
