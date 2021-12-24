import pygame
import constants as c
import gui.utils as utils
import sys

pygame.init()
game_big_font = pygame.font.SysFont(c.font_type, 45, True)

start_button_text = game_big_font.render("Start", True, c.white)
start_button_width = 140
start_button_height = 60
start_button_x = c.width / 2 - start_button_width / 2
start_button_y = c.height / 2 - start_button_height * 2

quit_button_text = game_big_font.render("Quit", True, c.white)
quit_button_width = 140
quit_button_height = 60
quit_button_x = c.width / 2 - start_button_width / 2
quit_button_y = c.height / 2


def start_menu(screen, background):
    while True:
        # create start button
        screen.blit(background, [0, 0])
        start_button = utils.create_button(screen, start_button_x, start_button_y, start_button_width,
                                           start_button_height, c.light_pink, c.pink)
        if start_button:
            break
        screen.blit(start_button_text,
                    (start_button_x + start_button_width / 6 - 2, start_button_y + start_button_height / 6))
        # create quit button
        quit_button = utils.create_button(screen, quit_button_x, quit_button_y, quit_button_width,
                                          quit_button_height, c.light_pink, c.pink)
        screen.blit(quit_button_text,
                    (quit_button_x + quit_button_width / 6, quit_button_y + quit_button_height / 6))
        if quit_button:
            utils.quit_window(screen, game_big_font, c.width / 4 + 25, c.height / 4 + 25, c.width / 4 + 225,
                              c.height / 4 + 150)

        utils.quit_event()

        pygame.display.update()
