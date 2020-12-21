TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3


class Tile:
    def __init__(self, tile_id, pattern):
        self.pattern = pattern
        self.tile_id = tile_id

        # Adjacent tiles that match the border
        self.top, self.bottom, self.left, self.right = None, None, None, None

    def get_border(self, location):
        if location == TOP:
            return self.pattern[0]
        elif location == BOTTOM:
            return self.pattern[-1]
        elif location == LEFT:
            return "".join([row[0] for row in self.pattern])
        elif location == RIGHT:
            return "".join([row[-1] for row in self.pattern])
        else:
            raise ValueError("Invalid location")

    def get_all_borders(self):
        return {TOP: self.get_border(TOP),
                BOTTOM: self.get_border(BOTTOM),
                LEFT: self.get_border(LEFT),
                RIGHT: self.get_border(RIGHT),}

    def rotate_right(self):
        new_pattern = []
        for i in range(len(self.pattern)):
            new_row = []
            for row in self.pattern:
                new_row.append(row[i])

            new_pattern.append("".join(reversed(new_row)))

        self.pattern = new_pattern


    def flip_vertical(self):
        size = len(self.pattern)
        for i in range(size // 2):
            temp_row = self.pattern[i]
            self.pattern[i] = self.pattern[size - i - 1]
            self.pattern[size - i - 1] = temp_row


def check_rotation_match(static_tile, mobile_tile):
    # Return True if through only the rotation of the mobile tile,
    # there is a matching pair of borders between both given tiles.
    for _ in range(4):
        tile.rotate_right()
        borders = tile.get_all_borders()

        if borders[TOP] == static_tile_borders[BOTTOM]:
            matches[BOTTOM].append(tile)
            return True
        if borders[BOTTOM] == static_tile_borders[TOP]:
            matches[TOP].append(tile)
            return True
        if borders[LEFT] == static_tile_borders[RIGHT]:
            matches[RIGHT].append(tile)
            return True
        if borders[RIGHT] == static_tile_borders[LEFT]:
            matches[LEFT].append(tile)
            return True

    return False


def get_match_data(static_tile, tiles):
    # Return matches, a dict containing (border position)-(matching tiles)
    # pairs, where matching borders is a list of all tiles which matches
    # the border of static_tile at border position when rotated and/or
    # reflected.
    static_tile_borders = static_tile.get_all_borders()
    matches = {TOP: [], BOTTOM: [], LEFT: [], RIGHT: [],}

    # Return True if through only the rotation of the mobile tile,
    # there is a matching pair of borders between both given tiles.
    def check_rotation_match(tile):
        for _ in range(4):
            tile.rotate_right()
            borders = tile.get_all_borders()

            if borders[TOP] == static_tile_borders[BOTTOM]:
                matches[BOTTOM].append(tile)
                return True
            if borders[BOTTOM] == static_tile_borders[TOP]:
                matches[TOP].append(tile)
                return True
            if borders[LEFT] == static_tile_borders[RIGHT]:
                matches[RIGHT].append(tile)
                return True
            if borders[RIGHT] == static_tile_borders[LEFT]:
                matches[LEFT].append(tile)
                return True

        return False

    for tile_n in tiles:
        tile = tiles[tile_n]
        if tile.tile_id == static_tile.tile_id:
            continue

        rotation_match = check_rotation_match(tile)
        if not rotation_match:
            # If rotating did not produce a match, reflect tile and try again
            tile.flip_vertical()
            if not check_rotation_match(tile):
                tile.flip_vertical()

    return matches


def part1():
    tiles = get_tiles()

    # Corner tiles only have 2 borders which match others
    corner_tiles = []
    for t in tiles:
        matches = get_match_data(tiles[t], tiles)
        if list(matches.values()).count([]) == 2:
            corner_tiles.append(t)

    prod = 1
    for n in corner_tiles:
        prod *= n

    return prod


def get_tiles():
    f = open("input.txt", "r")
    tiles = {}

    line = f.readline()
    while line:
        if "Tile" in line:
            tile_id = int(line.split()[1][:-1])
            tiles[tile_id] = Tile(tile_id, [])
        elif line != "\n":
            tiles[tile_id].pattern.append(line[:-1])

        line = f.readline()

    f.close()
    return tiles


if __name__ == "__main__":
    print(part1())
