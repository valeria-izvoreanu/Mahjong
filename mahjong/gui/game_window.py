import pygame
import constants as c
import gui.utils as utils
from random import randint

pygame.init()
game_big_font = pygame.font.SysFont(c.font_type, 45, True)
clock = pygame.time.Clock()


def game_screen(screen, background, option):
    x, y, tile_width, tile_height, table_type = get_table_type(option)
    tiles = get_tiles(tile_width, tile_height)
    table_array = get_tiles_table(utils.read_table_structure(table_type))
    write_to_file_table(table_array)

    start_time = None

    while True:
        screen.blit(background, [0, 0])
        # if first tile selected
        if start_time:
            time_since_fst_move = pygame.time.get_ticks() - start_time
        else:
            start_time = pygame.time.get_ticks()
            time_since_fst_move = 0
        con_sec, con_min, con_hour = utils.convert_millis(int(time_since_fst_move))
        up_screen(screen, 20, 5, con_sec, con_min, con_hour)
        side_screen(screen)

        draw_table(screen, tiles, table_array, x, y, tile_height, tile_width)

        utils.quit_event()
        pygame.display.update()
        clock.tick(60)


def up_screen(screen, tiles_nr, matches_nr, sec, minute, hour):
    pygame.draw.rect(screen, c.bright_pink,
                     pygame.Rect(0, 0, c.width, 60))

    utils.create_text(screen, game_big_font, "Tiles: " + str(tiles_nr), c.light_blue, 130, 10)
    utils.create_text(screen, game_big_font, "Matches: " + str(matches_nr), c.light_blue, 380, 10)
    time = "Time: " + "{hour_nr:02d}:{min_nr:02d}:{sec_nr:02d}".format(hour_nr=int(hour), min_nr=int(minute),
                                                                       sec_nr=int(sec))
    utils.create_text(screen, game_big_font, time, c.light_blue, 680, 10)


def make_side_button(screen, address, x, y, width, height):
    icon = utils.load_image(address, width - 10, height - 10)
    button = utils.create_button(screen, x, y, width, height, c.light_pink, c.dark_pink)
    screen.blit(icon, [x + 5, y + 5])
    return button


def side_screen(screen):
    pygame.draw.rect(screen, c.bright_pink,
                     pygame.Rect(c.width - 200, 60, 200, c.height))
    hint_btn = make_side_button(screen, "assets/hint_icon.png", c.width - 200 + 20, 150, 70, 70)
    help_btn = make_side_button(screen, "assets/help_icon.png", c.width - 200 + 110, 150, 70, 70)
    sound_btn = make_side_button(screen, "assets/sound_icon.png", c.width - 200 + 20, 240, 70, 70)
    undo_btn = make_side_button(screen, "assets/undo_icon.png", c.width - 200 + 110, 240, 70, 70)

    quit_btn = utils.create_button(screen, c.width - 155, 420, 110, 60, c.light_pink, c.dark_pink)
    utils.create_text(screen, game_big_font, "Quit", c.white, c.width - 155 + 10, 420 + 10)
    if quit_btn:
        utils.quit_window(screen, game_big_font, c.width / 4 + 25, c.height / 4 + 25, c.width / 4 + 225,
                          c.height / 4 + 150)


def get_table_type(option):
    if option == 1:
        return 25, 90, 50, 70, "turtle"
    elif option == 2:
        return 77.5, 92.5, 60, 80, "fortress"
    else:
        return 77.5, 75, 50, 65, "dragon"


def get_tiles(width, height):
    tiles = {}
    for i in range(42):
        tile_img = utils.load_image("assets/tiles/type1/t" + str(i + 1) + ".png", width, height)
        tiles["t" + str(i + 1)] = tile_img
    tiles["black"] = utils.load_image("assets/black_tile.png", width, height)
    return tiles


def get_random_tile(used_tiles):
    while True:
        value = randint(1, 42)
        if value < 35:
            if used_tiles[value - 1] < 4:
                return value
        else:
            if used_tiles[value - 1] < 2:
                return value


def get_tiles_table(table_array):
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


def write_to_file_table(table):
    file = open("assets/table.txt", "w")
    for layer in table:
        for line in layer:
            for elem in line:
                file.write(elem + " ")
            file.write("\n")
        file.write("\n")
    file.close()


def draw_table(screen, tiles, table_array, x, y, tile_height, tile_width):
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
                    if not utils.check_tile(table_array, x_coord, y_coord, z_coord):
                        screen.blit(black_tile, (x, y))
                    pygame.draw.rect(screen, color, pygame.Rect(x, y, tile_width, tile_height), 2)
                x += tile_width + 5
            x = x_abs
            y += tile_height + 5
        x_abs -= 5
        x = x_abs
        y_abs -= 5
        y = y_abs
        # if color == c.green:
        #    color = c.blue
        # else:
        #    color = c.green
