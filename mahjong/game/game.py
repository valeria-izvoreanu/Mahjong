def check_tile(table, x, y, z):
    if z + 1 < len(table):
        if table[z + 1][y][x] != '0':
            return False
    if x - 1 >= 0 and x + 1 < len(table[z][y]):
        if table[z][y][x - 1] != '0' and table[z][y][x + 1] != '0':
            return False
    return True


def check_if_tile_equal(table, tile1_coord, tile2_coord):
    tile1 = table[tile1_coord[2]][tile1_coord[1]][tile1_coord[0]]
    tile2 = table[tile2_coord[2]][tile2_coord[1]][tile2_coord[0]]
    if tile1 == tile2:
        return True
    if 35 <= int(tile1) <= 38 and 35 <= int(tile2) <= 38:
        return True
    if 39 <= int(tile1) <= 42 and 39 <= int(tile2) <= 42:
        return True
    return False


def update_array(table, tile1_coord, tile2_coord):
    table[tile1_coord[2]][tile1_coord[1]][tile1_coord[0]] = '0'
    table[tile2_coord[2]][tile2_coord[1]][tile2_coord[0]] = '0'
    tiles_count, matches_count = calculate_tiles_and_matches(table)
    return False, False, [-1, -1, -1], [-1, -1, -1], tiles_count, matches_count


def calculate_tiles_and_matches(table):
    matches = [0 for _ in range(42)]
    tiles_count = 0
    for z, layer in enumerate(table):
        for y, line in enumerate(layer):
            for x, elem in enumerate(line):
                if elem != '0':
                    tiles_count += 1
                    if check_tile(table, x, y, z):
                        matches[int(elem) - 1] += 1
    matches_count = 0
    for i in matches:
        if i > 1:
            matches_count += 1
    return tiles_count, matches_count
