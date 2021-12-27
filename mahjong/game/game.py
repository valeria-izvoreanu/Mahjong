"""
Contains function that solve the game logic of the app
"""


def check_tile(table, x, y, z):
    """
    Checks if tile is free, according to Mahjong rules.
    The rules are if there is no tile on top and at least one side(left, right) is free,
    the tile in question is free.
    :param table: list - 3-dimensional list that represents the table and the tiles
    :param x: int - the position in the line
    :param y: int - the line in which the tile is
    :param z: int - the layer on which the tile sits
    :return: bool - True if tile is free, False otherwise
    """
    if z + 1 < len(table):
        if table[z + 1][y][x] != '0':
            return False
    if x - 1 >= 0 and x + 1 < len(table[z][y]):
        if table[z][y][x - 1] != '0' and table[z][y][x + 1] != '0':
            return False
    return True


def check_if_tile_equal(table, tile1_coord, tile2_coord):
    """
    Checks if the same type of tiles were selected, or if flower(35 <= id <= 38) or season tiles (35 <= id <= 38)
    were selected, then checks if tiles belong in the same category.

    :param table: list - 3-dimensional list that represents the table and the tiles
    :param tile1_coord: list - [x,y,x] are the coordinates of tile 1 on the table
    :param tile2_coord: list - the coordinates of tile 2 on the table
    :return: bool - True, if the above conditions are fulfilled, False otherwise
    """
    tile1 = table[tile1_coord[2]][tile1_coord[1]][tile1_coord[0]]
    tile2 = table[tile2_coord[2]][tile2_coord[1]][tile2_coord[0]]
    if tile1 == tile2:
        return True
    if 35 <= int(tile1) <= 38 and 35 <= int(tile2) <= 38:
        return True
    if 39 <= int(tile1) <= 42 and 39 <= int(tile2) <= 42:
        return True
    return False


def update_array(table, tile1_coord, tile2_coord, value1='0', value2='0'):
    """
    Update table and write '0' in the positions of th removed tiles,
    recalculate the number of tiles and the possible matches.

    :param table: list - 3-dimensional list that represents the table and the tiles
    :param tile1_coord: list - [x,y,x] are the coordinates of tile 1 on the table
    :param tile2_coord: list - the coordinates of tile 2 on the table
    :param value1: str - id of tile 1
    :param value2: str - id of tile 2
    :return: bool - state of tile 1;
             bool - state of tile 2;
             list - coordinates of tile 1;
             list - coordinates of tile 2;
             int - total of tiles on the table;
             list - all possible matches
    """
    table[tile1_coord[2]][tile1_coord[1]][tile1_coord[0]] = value1
    table[tile2_coord[2]][tile2_coord[1]][tile2_coord[0]] = value2
    tiles_count, matches = calculate_tiles_and_matches(table)
    return False, False, [-1, -1, -1], [-1, -1, -1], tiles_count, matches


def calculate_tiles_and_matches(table):
    """
    Calculates the number of tiles on the table and all the possible matches
    :param table: list - 3-dimensional list that represents the table and the tiles
    :return: int - total of tiles on the table;
             list - all possible matches
    """
    tiles = [[] for _ in range(42)]
    matches = []
    tiles_count = 0
    for z, layer in enumerate(table):
        for y, line in enumerate(layer):
            for x, elem in enumerate(line):
                if elem != '0':
                    tiles_count += 1
                    if check_tile(table, x, y, z):
                        if len(tiles[int(elem) - 1]) == 0:
                            tiles[int(elem) - 1] = []
                        else:
                            for tile in tiles[int(elem) - 1]:
                                matches.append([(x, y, z), tile])
                        tiles[int(elem) - 1].append((x, y, z))
    return tiles_count, matches
