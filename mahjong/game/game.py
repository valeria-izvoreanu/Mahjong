def check_tile(table, x, y, z):
    if z + 1 < len(table):
        if table[z + 1][y][x] != '0':
            return False
    if x - 1 >= 0 and x + 1 < len(table[z][y]):
        if table[z][y][x - 1] != '0' and table[z][y][x + 1] != '0':
            return False
    return True


def check_if_tile_equal(table, tile1_coord, tile2_coord):
    if table[tile1_coord[2]][tile1_coord[1]][tile1_coord[0]] == table[tile2_coord[2]][tile2_coord[1]][tile2_coord[0]]:
        return True
    return False


def update_array(table, tile1_coord, tile2_coord):
    table[tile1_coord[2]][tile1_coord[1]][tile1_coord[0]] = '0'
    table[tile2_coord[2]][tile2_coord[1]][tile2_coord[0]] = '0'
    return False, False, [-1, -1, -1], [-1, -1, -1]
