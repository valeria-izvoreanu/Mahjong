import pygame
import constants as c
import gui.utils as utils

pygame.init()
game_big_font = pygame.font.SysFont(c.font_type, 45, True)
clock = pygame.time.Clock()


def game_screen(screen, background, option):
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
    icon = pygame.image.load(address).convert_alpha()
    icon = pygame.transform.scale(icon, (width - 10, height - 10))
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
