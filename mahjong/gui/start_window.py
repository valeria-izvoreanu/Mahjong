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
        screen.blit(background, [0, 0])
        start_button = utils.create_button(screen, start_button_x, start_button_y, start_button_width,
                                           start_button_height, c.light_pink, c.pink)
        if start_button:
            break
        screen.blit(start_button_text,
                    (start_button_x + start_button_width / 6 - 2, start_button_y + start_button_height / 6))

        quit_button = utils.create_button(screen, quit_button_x, quit_button_y, quit_button_width,
                                          quit_button_height, c.light_pink, c.pink)
        if quit_button:
            pygame.quit()
            sys.exit()
        screen.blit(quit_button_text,
                    (quit_button_x + quit_button_width / 6, quit_button_y + quit_button_height / 6))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
