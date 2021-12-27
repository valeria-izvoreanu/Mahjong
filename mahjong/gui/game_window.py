"""
This is the file that make the graphics on which the user can play the game
"""

import pygame
import constants as c
import gui.utils as utils
from random import randint
import game.game as game
import sys
import gui.start_window as start

pygame.init()
game_big_font = pygame.font.SysFont(c.font_type, 45, True)
clock = pygame.time.Clock()

start_time = None
sound = "sound"

matches = []  # possible matches, matches[i]=[(x1,y1,z1), (x2,y2,z2)]
hint_nr = 0
hint = None

moves = []  # all previous moves, moves[i]=[(x1,y1,z1), (x2,y2,z2)]


def init_game(screen, background, option):
    """
    Initialises all game parameters.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param background: pygame.Surface - the background image
    :param option: int - number which corresponds to one table type
    """
    global matches, moves, start_time, sound
    moves = []
    start_time = None
    sound = "sound"
    x, y, tile_width, tile_height, table_type = get_table_type(option)

    # load tiles images and read table from corresponding file
    tiles = get_tiles(tile_width, tile_height)
    table_array = get_tiles_table(utils.read_table_structure(table_type))

    tile_count, matches = game.calculate_tiles_and_matches(table_array)

    game_screen(screen, background, x, y, tile_width, tile_height, table_type, tiles, table_array, tile_count)


def game_screen(screen, background, x, y, tile_width, tile_height, table_type, tiles, table_array, tile_count):
    """
    Makes the game screen on which the game is played and manages the game play.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param background: pygame.Surface - the background image
    :param x: float/int - upper x-coordinate of table
    :param y: float/int - upper y-coordinate of table
    :param tile_width: int
    :param tile_height: int
    :param table_type: str
    :param tiles: dict - dictionary that corresponds tile name of the type: t1(example) to a pygame.Surface
                         that is the image of the tile
    :param table_array: list - 3-dimensional list that represents the table and the tiles.
                               If list[z][y][x] == '0' there is no tile on that position, otherwise, there is a number
                               that corresponds to the name in the tiles dictionary.
                               The indexes are: z - is the layer on which the tile sits
                                                y - is the line
                                                x - is the position in the line
    :param tile_count: int - total of tiles on the table at the moment
    """
    tile1 = False
    tile2 = False

    tile1_coord = [-1, -1, -1]
    tile2_coord = [-1, -1, -1]

    global matches
    time_since_fst_move = 0

    while True:
        screen.blit(background, [0, 0])
        if tile_count > 0 and len(matches) > 0:
            # get time and start clock only when player clicks on first tile
            if start_time is not None:
                time_since_fst_move = pygame.time.get_ticks() - start_time
            else:
                time_since_fst_move = 0
            con_sec, con_min, con_hour = utils.convert_millis(int(time_since_fst_move))

            up_screen(screen, tile_count, len(matches), con_sec, con_min, con_hour)
            side_screen(screen)

            tile1, tile2, tile1_coord, tile2_coord = draw_table(screen, tiles, table_array, x, y, tile_height,
                                                                tile_width,
                                                                tile1, tile2, tile1_coord, tile2_coord)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    tile1, tile2, tile1_coord, tile2_coord, tile_count = click_event(screen, table_array, x,
                                                                                     y, tile_width,
                                                                                     tile_height,
                                                                                     pos[0], pos[1], tile1,
                                                                                     tile2, tile1_coord,
                                                                                     tile2_coord, tile_count)
            clock.tick(60)
        elif tile_count == 0:
            winning_screen(screen, background, time_since_fst_move, table_type,
                           c.width / 2 - (c.width / 1.9 + 225) / 2,
                           c.height / 4 - 55, c.width / 1.9 + 225,
                           c.height / 1.9 + 150)
        elif len(matches) == 0:
            loosing_screen(screen, background, c.width / 2 - (c.width / 1.9 + 225) / 2,
                           c.height / 4 - 55, c.width / 1.9 + 225,
                           c.height / 1.9 + 150)
            tile1, tile2, tile1_coord, tile2_coord, tile_count, matches = undo_move(table_array, tile1, tile2,
                                                                                    tile1_coord, tile2_coord,
                                                                                    tile_count)
        pygame.display.update()


def get_table_type(option):
    """
    Computes table type depending on option chosen by player in starting window.

    :param option: int
    :return: float/int - upper x-coordinate of table;
             float/int - upper y-coordinate of table;
             int - tile width;
             int - tile height;
             str - table name
    """
    if option == 1:
        return 25, 90, 50, 70, "turtle"
    elif option == 2:
        return 77.5, 92.5, 60, 80, "fortress"
    else:
        return 77.5, 75, 50, 65, "dragon"


def get_tiles(width, height):
    """
    Loads tiles' images from assets/type1 folder and saves them in a dictionary.

    :param width: tile image width
    :param height: tile image height
    :return: dictionary that corresponds tile name of the type: t1(example) to a pygame.Surface
             that is the image of the tile
    """
    tiles = {}
    for i in range(42):
        tile_img = utils.load_image("assets/tiles/type1/t" + str(i + 1) + ".png", width, height)
        tiles["t" + str(i + 1)] = tile_img
    tiles["black"] = utils.load_image("assets/black_tile.png", width, height)
    return tiles


def get_random_tile(used_tiles):
    """
    Calculates a random number that corresponds to a tile respecting restrictions of the game,
    such as, there should be 4 tiles of each type,
    except flower tiles and season tiles(those with id >= 35) that can be 2 of each type.

    :param used_tiles: list - keeps track of tiles already placed on the table and
                              assures that the restrictions are fulfilled
    :return: int - id of new tile
    """
    while True:
        value = randint(1, 42)
        if value < 35:
            if used_tiles[value - 1] < 4:
                return value
        else:
            if used_tiles[value - 1] < 2:
                return value


def get_tiles_table(table_array):
    """
    Computes the table by choosing random values to place in the available positions

    :param table_array: list - 3-dimensional array that represents the structure of the table
                               if element from list is equal with '1', a tile can be placed in that position
    :return: list - 3-dimensional array that represents the structure of the table
                    if element from list is different from '0', a tile has been placed in that position
    """
    used_tiles = [0 for _ in range(42)]
    table_tiles = [[[]]]
    layer_index = 0
    line_index = 0
    for layer in table_array:
        for line in layer:
            for elem in line:
                if elem == '1':
                    new_tile = get_random_tile(used_tiles)
                    table_tiles[layer_index][line_index].append(str(new_tile))
                    used_tiles[new_tile - 1] += 1
                else:
                    table_tiles[layer_index][line_index].append("0")
            if line_index < len(layer) - 1:
                table_tiles[layer_index].append([])
            line_index += 1
        if layer_index < len(table_array) - 1:
            table_tiles.append([[]])
        layer_index += 1
        line_index = 0
    return table_tiles


def up_screen(screen, tiles_nr, matches_nr, sec, minute, hour):
    """
    Draws the part of game window at the top of the screen.
    It displays number of tiles left, number of possible matches and the time since first tile pressed.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param tiles_nr: int - total of tiles on the table at the moment
    :param matches_nr: int - number of possible matches
    :param sec: float
    :param minute: float
    :param hour: float
    """
    pygame.draw.rect(screen, c.bright_pink,
                     pygame.Rect(0, 0, c.width, 60))

    utils.create_text(screen, game_big_font, "Tiles: " + str(tiles_nr), c.light_blue, 130, 10)
    utils.create_text(screen, game_big_font, "Matches: " + str(matches_nr), c.light_blue, 380, 10)
    time = "Time: " + "{hour_nr:02d}:{min_nr:02d}:{sec_nr:02d}".format(hour_nr=int(hour), min_nr=int(minute),
                                                                       sec_nr=int(sec))
    utils.create_text(screen, game_big_font, time, c.light_blue, 680, 10)


def side_screen(screen):
    """
    Draws the right side of the window which contains buttons that allow:
        hint button: gives a hint to the player
        help button: opens help pop up that explain the rules of the game
        sound button: lets player turn on/off music
        undo button: lets player undo moves

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    """
    pygame.draw.rect(screen, c.bright_pink,
                     pygame.Rect(c.width - 200, 60, 200, c.height))
    make_side_button(screen, "assets/hint_icon.png", c.width - 200 + 20, 150, 70, 70)
    make_side_button(screen, "assets/help_icon.png", c.width - 200 + 110, 150, 70, 70)
    make_side_button(screen, "assets/" + sound + "_icon.png", c.width - 200 + 20, 240, 70, 70)
    make_side_button(screen, "assets/undo_icon.png", c.width - 200 + 110, 240, 70, 70)

    utils.create_button(screen, c.width - 155, 420, 110, 60, c.light_pink, c.dark_pink)
    utils.create_text(screen, game_big_font, "Quit", c.white, c.width - 155 + 10, 420 + 10)


def draw_table(screen, tiles, table_array, x, y, tile_height, tile_width, tile1, tile2, tile1_coord, tile2_coord):
    """
    Draws the table and the selected/ hinted tiles.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param tiles: dict - dictionary that corresponds tile name of the type: t1(example) to a pygame.Surface
                         that is the image of the tile
    :param table_array: list - 3-dimensional list that represents the table and the tiles.
    :param x: float/int - upper x-coordinate of table
    :param y: float/int - upper y-coordinate of table
    :param tile_height: int
    :param tile_width: int
    :param tile1: bool - True if a tile has been selected and False otherwise
    :param tile2: bool - True if a second tile has been selected and False otherwise
    :param tile1_coord: list - saves the coordinates of a selected tile
                               in the form [x,y,z](with the aforementioned meanings)
                               x = y = z = -1 if no tile is selected
    :param tile2_coord: list - saves the coordinates of the second selected tile
    :return: bool - True if a tile has been selected and False otherwise;
             bool - True if a second tile has been selected and False otherwise;
             list - saves the coordinates of a selected tile;
             list - saves the coordinates of the second selected tile
    """
    x_layer = x
    y_layer = y
    x_abs = x
    y_abs = y
    color = c.green
    black_tile = tiles["black"]
    pygame.Surface.set_alpha(black_tile, 100)
    for z_coord, layer in enumerate(table_array):
        for y_coord, line in enumerate(layer):
            for x_coord, elem in enumerate(line):
                if elem != '0':
                    tile = tiles["t" + elem]
                    screen.blit(tile, (x, y))
                    # if tile is blocked, draw a black square on top
                    if not game.check_tile(table_array, x_coord, y_coord, z_coord):
                        screen.blit(black_tile, (x, y))
                        pygame.draw.rect(screen, color, pygame.Rect(x, y, tile_width, tile_height), 2)
                    else:
                        hover_tile(screen, x, y, tile_width, tile_height)
                x += tile_width + 5
            x = x_layer
            y += tile_height + 5
        x_layer -= 5
        x = x_layer
        y_layer -= 5
        y = y_layer
    if tile1:
        draw_tile_square(screen, x_abs, y_abs, tile_width, tile_height, tile1_coord, c.bright_pink)
    if tile2:
        draw_tile_square(screen, x_abs, y_abs, tile_width, tile_height, tile2_coord, c.bright_pink)
    global hint
    if hint is not None:
        draw_tile_square(screen, x_abs, y_abs, tile_width, tile_height, hint[0], c.dark_blue)
        draw_tile_square(screen, x_abs, y_abs, tile_width, tile_height, hint[1], c.dark_blue)
    return tile1, tile2, tile1_coord, tile2_coord


def make_side_button(screen, address, x, y, width, height):
    """
    Creates buttons on the side screen.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param address: str
    :param x: int - upper x-coordinate of button
    :param y: int - upper y-coordinate of button
    :param width: int - width of button
    :param height: int - height of button
    """
    icon = utils.load_image(address, width - 10, height - 10)
    utils.create_button(screen, x, y, width, height, c.light_pink, c.dark_pink)
    screen.blit(icon, [x + 5, y + 5])


def hover_tile(screen, x, y, width, height):
    """
    Creates the hover animation
    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param x: float - upper x-coordinate of tile on the screen
    :param y: float - upper y-coordinate of tile on the screen
    :param width: int - width of tile
    :param height: int - height of tile
    """
    mouse = pygame.mouse.get_pos()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, c.bright_pink, pygame.Rect(x, y, width, height), 2)
    else:
        pygame.draw.rect(screen, c.green, pygame.Rect(x, y, width, height), 2)


def get_tile_coord(x_abs, y_abs, tile_width, tile_height, tile_coord):
    """
    Calculate the x, y coordinates on the screen from the tile coordinates in the table array.

    :param x_abs: float/int - upper x-coordinate of table
    :param y_abs: float/int - upper y-coordinate of table
    :param tile_width: int
    :param tile_height: int
    :param tile_coord: list - the coordinates of the tile in the form [x,y,z](with the aforementioned meanings)
    :return: float/int - x-coordinate on the screen;
             float/int - y-coordinate on the screen
    """
    x_tile = x_abs - 5 * tile_coord[2] + (tile_width + 5) * tile_coord[0]
    y_tile = y_abs - 5 * tile_coord[2] + (5 + tile_height) * tile_coord[1]
    return x_tile, y_tile


def draw_tile_square(screen, x_abs, y_abs, tile_width, tile_height, tile_coord, color):
    """
    Draw the square around the selected/hinted tile.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param x_abs: float/int - upper x-coordinate of table
    :param y_abs: float/int - upper y-coordinate of table
    :param tile_width: int
    :param tile_height: int
    :param tile_coord: list - the coordinates of the tile in the form [x,y,z](with the aforementioned meanings)
    :param color: tuple - RGB colour
    """
    x_tile, y_tile = get_tile_coord(x_abs, y_abs, tile_width, tile_height, tile_coord)
    pygame.draw.rect(screen, color, pygame.Rect(x_tile, y_tile, tile_width, tile_height), 2)


def click_event(screen, table_array, x_abs, y_abs, tile_width, tile_height, x, y, tile1, tile2, tile1_coord,
                tile2_coord, tile_count):
    """
    Handles the player's click.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param table_array: list - 3-dimensional list that represents the table and the tiles
    :param x_abs: float/int - upper x-coordinate of table
    :param y_abs: float/int - upper y-coordinate of table
    :param tile_width: int
    :param tile_height: int
    :param x: float - x-coordinate of player click
    :param y: float - y-coordinate of player click
    :param tile1: bool - True if a tile has been selected and False otherwise
    :param tile2: bool - True if a second tile has been selected and False otherwise
    :param tile1_coord: list - saves the coordinates of a selected tile
    :param tile2_coord: list - saves the coordinates of the second selected tile
    :param tile_count: int - total of tiles on the table at the moment
    :return: bool - True if a tile has been selected and False otherwise;
             bool - True if a second tile has been selected and False otherwise;
             list - saves the coordinates of a selected tile;
             list - saves the coordinates of the second selected tile;
             int - total of tiles on the table at the moment
    """
    global hint
    # if click in table area
    if x < (c.width - 200) and y > 60:
        tile1, tile2, tile1_coord, tile2_coord, tile_count = click_table_event(table_array, x_abs, y_abs,
                                                                               tile_width, tile_height,
                                                                               x, y, tile1, tile2,
                                                                               tile1_coord,
                                                                               tile2_coord, tile_count)
        hint = None
    # if click in side area
    elif y > 60:
        if c.width - 155 < x < c.width - 155 + 110 and 420 < y < 480:
            utils.quit_window(screen, game_big_font, c.width / 4 + 25, c.height / 4 + 25, c.width / 4 + 225,
                              c.height / 4 + 150)
            hint = None
        if c.width - 200 + 20 < x < c.width - 200 + 90 and 240 < y < 310:
            handle_music()
            hint = None
        if c.width - 200 + 110 < x < c.width - 200 + 180 and 150 < y < 220:
            show_help_menu(screen, (c.width - 200) / 2 - (c.width / 1.9 + 225) / 2,
                           (c.height - 60) / 4 - 55, c.width / 1.9 + 225,
                           c.height / 1.9 + 150)
            hint = None
        if c.width - 200 + 20 < x < c.width - 200 + 90 and 150 < y < 220:
            hint = get_hint()
        if c.width - 200 + 110 < x < c.width - 200 + 180 and 240 < y < 310:
            global matches
            tile1, tile2, tile1_coord, tile2_coord, tile_count, matches = undo_move(table_array, tile1, tile2,
                                                                                    tile1_coord, tile2_coord,
                                                                                    tile_count)

    return tile1, tile2, tile1_coord, tile2_coord, tile_count


def click_table_event(table_array, x_abs, y_abs, tile_width, tile_height, x, y, tile1, tile2, tile1_coord,
                      tile2_coord, tile_count):
    """
    Handle click in the table area of the screen.

    :param table_array: list - 3-dimensional list that represents the table and the tiles
    :param x_abs: float/int - upper x-coordinate of table
    :param y_abs: float/int - upper y-coordinate of table
    :param tile_width: int
    :param tile_height: int
    :param x: float - x-coordinate of player click
    :param y: float - y-coordinate of player click
    :param tile1: bool - True if a tile has been selected and False otherwise
    :param tile2: bool - True if a second tile has been selected and False otherwise
    :param tile1_coord: list - saves the coordinates of a selected tile
    :param tile2_coord: list - saves the coordinates of the second selected tile
    :param tile_count: int - total of tiles on the table at the moment
    :return: bool - True if a tile has been selected and False otherwise;
             bool - True if a second tile has been selected and False otherwise;
             list - saves the coordinates of a selected tile;
             list - saves the coordinates of the second selected tile;
             int - total of tiles on the table at the moment
    """
    global start_time, matches
    if not start_time:
        start_time = pygame.time.get_ticks()
    # compute table coordinates
    x_coord = int((x - x_abs) // (tile_width + 5))
    y_coord = int((y - y_abs) // (tile_height + 5))
    z_coord = -1
    count = len(table_array) - 1
    for layer in reversed(table_array):
        if layer[y_coord][x_coord] != '0':
            z_coord = count
            break
        count -= 1
    # if one of the coordinates is -1, player didn't click any tile
    if z_coord != -1 and x_coord != -1 and y_coord != -1:
        if game.check_tile(table_array, x_coord, y_coord, z_coord):
            # if not tile selected update tile1
            if not tile1:
                tile1, tile1_coord[0], tile1_coord[1], tile1_coord[2] = True, x_coord, y_coord, z_coord
            else:
                # if a tile is selected update tile2
                tile2, tile2_coord[0], tile2_coord[1], tile2_coord[2] = True, x_coord, y_coord, z_coord
                # if same tile was selected, deselect it
                if tile1_coord == tile2_coord:
                    tile2 = False
                    tile2_coord = [-1, -1, -1]
                    tile1 = False
                    tile1_coord = [-1, -1, -1]
                # if a different tile was selected, check if move was valid
                # if yes, remove tiles, if no, tile1 becomes tile2
                if tile2:
                    if game.check_if_tile_equal(table_array, tile1_coord, tile2_coord):
                        update_moves(table_array[tile1_coord[2]][tile1_coord[1]][tile1_coord[0]],
                                     table_array[tile2_coord[2]][tile2_coord[1]][tile2_coord[0]], list(tile1_coord),
                                     list(tile2_coord))
                        tile1, tile2, tile1_coord, tile2_coord, tile_count, matches = game.update_array(
                            table_array, tile1_coord, tile2_coord)
                    else:
                        tile2 = False
                        tile1_coord = list(tile2_coord)
                        tile2_coord = [-1, -1, -1]
    else:
        tile1 = False
        tile1_coord = [-1, -1, -1]
    return tile1, tile2, tile1_coord, tile2_coord, tile_count


def update_moves(value1, value2, tile1_coord, tile2_coord):
    """
    Update global list moves, appends new move

    :param value1: str - id of tile 1
    :param value2: str - id of tile 2
    :param tile1_coord: list - coordinates of tile 1
    :param tile2_coord: list - coordinates of tile 2
    """
    tile1_coord.append(value1)
    tile2_coord.append(value2)
    moves.append([tile1_coord, tile2_coord])


def undo_move(table_array, tile1, tile2, tile1_coord, tile2_coord, tile_count):
    """
    Performs undo move.

    :param table_array: list - 3-dimensional list that represents the table and the tiles
    :param tile1: bool - True if a tile has been selected and False otherwise
    :param tile2: bool - True if a second tile has been selected and False otherwise
    :param tile1_coord: list - saves the coordinates of a selected tile
    :param tile2_coord: list - saves the coordinates of the second selected tile
    :param tile_count: int - total of tiles on the table at the moment
    :return: bool - True if a tile has been selected and False otherwise;
             bool - True if a second tile has been selected and False otherwise;
             list - saves the coordinates of a selected tile;
             list - saves the coordinates of the second selected tile;
             int - total of tiles on the table at the moment
             list - list of all possible matches
    """
    global moves, matches
    if len(moves) > 0:
        last_move = moves.pop()
        return game.update_array(table_array, last_move[0], last_move[1], last_move[0][3], last_move[1][3])
    return tile1, tile2, tile1_coord, tile2_coord, tile_count, matches


def get_hint():
    """
    Return a possible tile match.
    :return: list - coordinates of the tiles that form a match
    """
    global hint_nr, matches
    # if all hints have been shown, start again from the first one
    if hint_nr < len(matches):
        hint_nr += 1
        return matches[hint_nr - 1]
    else:
        hint_nr = 0
        return matches[hint_nr]


def handle_music():
    """
    Turns on/off the music
    """
    global sound
    if sound == "mute":
        pygame.mixer.music.unpause()
        sound = "sound"
    else:
        pygame.mixer.music.pause()
        sound = "mute"


def show_help_menu(screen, x, y, width, height):
    """
    Displays help screen
    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param x: float - upper x-coordinate of help screen
    :param y: float - upper y-coordinate of help screen
    :param width: float - width of help screen
    :param height: float height of help screen
    """
    close_button_text = game_big_font.render("Close", True, c.white)
    close_button_width = 140
    close_button_height = 60
    close_button_x = x + width / 2 - close_button_width / 2
    close_button_y = y + height / 1.17
    img = utils.load_image("assets/help.png", width, height)
    while True:
        pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, width, height), 5)
        screen.blit(img, (x, y))
        close_button = utils.create_button(screen, close_button_x, close_button_y, close_button_width,
                                           close_button_height, c.light_pink, c.blue)
        screen.blit(close_button_text,
                    (close_button_x + close_button_width / 6 - 2, close_button_y + close_button_height / 6))
        if close_button:
            return
        utils.quit_event()
        pygame.display.update()


def loosing_screen(screen, background, x, y, height, width):
    """
    Displays losing screen.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param background: pygame.Surface - the background image
    :param x: float - upper x-coordinate of window
    :param y: float - upper y-coordinate of window
    :param height: float - height of window
    :param width: float - width of window
    """
    new_button_text = game_big_font.render("New Game", True, c.bright_pink)
    new_button_width = 300
    new_button_height = 60
    new_button_x = x + 100
    new_button_y = y + 400

    no_button_text = game_big_font.render("Exit", True, c.bright_pink)
    no_button_width = 120
    no_button_height = 60
    no_button_x = x + 550
    no_button_y = y + 400

    undo_button_text = game_big_font.render("Undo last move", True, c.bright_pink)
    undo_button_width = 450
    undo_button_height = 60
    undo_button_x = x + 170
    undo_button_y = y + 300
    while True:
        pygame.draw.rect(screen, c.bright_pink,
                         pygame.Rect(x, y, height, width))
        pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, height, width), 3)

        text = "You lost!"
        utils.create_text(screen, game_big_font, text, c.light_blue, x + width / 2 + 40, y + 80)

        text = "No more matches left!"
        text_width = game_big_font.size(text)[0]
        text_height = game_big_font.size(text)[1]
        utils.create_text(screen, game_big_font, text, c.light_blue, x + width / 2 - text_width / 5,
                          y + text_height + 95)

        new_button = utils.create_button(screen, new_button_x, new_button_y, new_button_width,
                                         new_button_height, c.light_pink, c.blue)
        screen.blit(new_button_text,
                    (new_button_x + new_button_width / 6 - 2, new_button_y + new_button_height / 6))

        if new_button:
            start.start_menu(screen, background)

        no_button = utils.create_button(screen, no_button_x, no_button_y, no_button_width,
                                        no_button_height, c.light_pink, c.blue)
        screen.blit(no_button_text,
                    (no_button_x + no_button_width / 6 - 2, no_button_y + no_button_height / 6))

        if no_button:
            pygame.quit()
            sys.exit()

        undo_button = utils.create_button(screen, undo_button_x, undo_button_y, undo_button_width,
                                          undo_button_height, c.light_pink, c.blue)
        screen.blit(undo_button_text,
                    (undo_button_x + undo_button_width / 6 - 2, undo_button_y + undo_button_height / 6))

        if undo_button:
            return

        utils.quit_event()
        pygame.display.update()


def winning_screen(screen, background, time_since_fst_move, table_type, x, y, height, width):
    """
    Displays winning screen.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param background: pygame.Surface - the background image
    :param time_since_fst_move: int -how long it took the player to win
    :param table_type: str
    :param x: float - upper x-coordinate of window
    :param y: float - upper y-coordinate of window
    :param height: float - height of window
    :param width: float - width of window
    """
    new_button_text = game_big_font.render("New Game", True, c.bright_pink)
    new_button_width = 300
    new_button_height = 60
    new_button_x = x + 100
    new_button_y = y + 400

    no_button_text = game_big_font.render("Exit", True, c.bright_pink)
    no_button_width = 120
    no_button_height = 60
    no_button_x = x + 500
    no_button_y = y + 400
    while True:
        screen.blit(background, [0, 0])
        pygame.draw.rect(screen, c.bright_pink,
                         pygame.Rect(x, y, height, width))
        pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, height, width), 3)

        sec, minute, hour = utils.convert_millis(int(time_since_fst_move))

        text = "Congratulations!"
        text_width = game_big_font.size(text)[0]
        utils.create_text(screen, game_big_font, text, c.light_blue, x + width / 2 - text_width / 6, y + 80)

        text = "You completed the " + table_type + " table!"
        text_width = game_big_font.size(text)[0]
        text_height = game_big_font.size(text)[1]
        utils.create_text(screen, game_big_font, text, c.light_blue, x + width / 2 - text_width / 3.5,
                          y + text_height + 95)

        text = "Your time: " + "{hour_nr:02d}:{min_nr:02d}:{sec_nr:02d}".format(hour_nr=int(hour),
                                                                                min_nr=int(minute),
                                                                                sec_nr=int(sec))
        text_width = game_big_font.size(text)[0]
        utils.create_text(screen, game_big_font, text, c.light_blue, x + width / 2 - text_width / 6,
                          y + text_height * 2 + 110)

        new_button = utils.create_button(screen, new_button_x, new_button_y, new_button_width,
                                         new_button_height, c.light_pink, c.blue)
        screen.blit(new_button_text,
                    (new_button_x + new_button_width / 6 - 2, new_button_y + new_button_height / 6))

        if new_button:
            start.start_menu(screen, background)

        no_button = utils.create_button(screen, no_button_x, no_button_y, no_button_width,
                                        no_button_height, c.light_pink, c.blue)
        screen.blit(no_button_text,
                    (no_button_x + no_button_width / 6 - 2, no_button_y + no_button_height / 6))

        if no_button:
            pygame.quit()
            sys.exit()

        utils.quit_event()
        pygame.display.update()
