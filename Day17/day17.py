CYCLES = 6


class Cube:
    def __init__(self, active, adj_active=0):
        self.active = active
        self.adj_active = adj_active


def simulate(dimension):
    # Store only active cubes as coordinates (x, y, z)
    # Assume dimension >= 2
    f = open("input.txt", "r")
    lines = [line[:-1] for line in f.readlines()]

    active_cubes = {}

    # Store all initially active cubes
    for x, row in enumerate(lines):
        for y, cube in enumerate(row):
            if cube == "#":
                coord = (x, y)
                for _ in range(dimension - 2):
                    coord += (0,)

                active_cubes[coord] = Cube(True)

    # Also store all inactive cubes adjacent to active cubes, and set
    # all cubes' active neighbour count
    cubes = active_cubes.copy()
    set_adj_cubes(active_cubes, cubes)

    for _ in range(CYCLES):
        cubes = update_state(cubes)

    result = 0
    for coords in cubes:
        if cubes[coords].active:
            result += 1

    return result


def get_neighbours(*coords):
    result = []
    dimensions = len(coords)

    def get_neighbours_rec(dim, rsf):
        if dim == dimensions:
            result.append(rsf)
        else:
            for x in range(coords[dim] - 1, coords[dim] + 2):
                get_neighbours_rec(dim + 1, rsf + (x,))

    get_neighbours_rec(0, ())
    result.remove(coords)
    return result


def set_adj_cubes(active_cubes, dest_cubes):
    for k in active_cubes:
        adj_cubes_coords = get_neighbours(*k)
        for coords in adj_cubes_coords:
            if not dest_cubes.get(coords):
                dest_cubes[coords] = Cube(False, 1)
            else:
                dest_cubes[coords].adj_active += 1



def update_state(cubes):
    new_active_cubes = {}

    # Find all next active cubes
    for coord in cubes:
        cube = cubes[coord]
        if (cube.active and cube.adj_active in [2, 3] or
            not cube.active and cube.adj_active == 3):
            new_active_cubes[coord] = Cube(True)

    new_state = new_active_cubes.copy()

    # Store all inactive cubes adjacent to active cubes,
    # and set adj cube count
    set_adj_cubes(new_active_cubes, new_state)

    return new_state


if __name__ == "__main__":
    print(simulate(dimension=3))
    print(simulate(dimension=4))
