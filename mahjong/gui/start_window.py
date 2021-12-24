import pygame
import constants as c
import gui.utils as utils
import sys

pygame.init()
game_big_font = pygame.font.SysFont(c.font_type, 45, True)


def start_menu(screen, background):
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
    while True:
        # create start button
        screen.blit(background, [0, 0])
        start_button = utils.create_button(screen, start_button_x, start_button_y, start_button_width,
                                           start_button_height, c.light_pink, c.pink)
        if start_button:
            table_menu(screen, background)
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


def draw_table_option(screen, text, x, y, width, height):
    pygame.draw.rect(screen, c.bright_pink,
                     pygame.Rect(x, y, width, height))
    pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, width, height), 3)
    option_name = game_big_font.render(text, True, c.light_blue)
    option_button = utils.create_button(screen, x, y + height + 20, width,
                                        50, c.light_pink, c.bright_pink)
    text_width = game_big_font.size(text)[0]
    screen.blit(option_name, (x + width / 2 - text_width / 2, height + 265))
    return option_button


def draw_selected_square(screen, text, x, y, width, height):
    pygame.draw.rect(screen, c.bright_pink,
                     pygame.Rect(x, y, width, height))
    pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, width, height), 3)
    pygame.draw.rect(screen, c.light_pink,
                     pygame.Rect(x, y + height + 20, width, 50))
    pygame.draw.rect(screen, c.blue, pygame.Rect(x, y + height + 20, width, 50), 3)
    option_name = game_big_font.render(text, True, c.blue)
    text_width = game_big_font.size(text)[0]
    screen.blit(option_name, (x + width / 2 - text_width / 2, height + 265))


def table_menu(screen, background):
    text = game_big_font.render("Choose Table Type:", True, c.bright_pink)
    option = 0
    option1 = False
    option2 = False
    option3 = False

    start_button_text = game_big_font.render("Start", True, c.light_blue)
    start_button_width = 140
    start_button_height = 60
    start_button_x = c.width / 2 - start_button_width / 2
    start_button_y = c.height - start_button_height * 1.5
    while True:
        screen.blit(background, [0, 0])
        screen.blit(text, (c.width / 3, c.height / 6))

        if option1:
            draw_selected_square(screen, "Turtle", c.width / 17, c.height / 3, 270, c.height / 3 + 50)
            option2 = draw_table_option(screen, "Fortress", c.width / 17 + 270 + 70, c.height / 3, 270,
                                        c.height / 3 + 50)
            option3 = draw_table_option(screen, "Dragon", c.width / 17 + 270 * 2 + 70 * 2, c.height / 3, 270,
                                        c.height / 3 + 50)
            option = 1

        if option2:
            draw_selected_square(screen, "Fortress", c.width / 17 + 270 + 70, c.height / 3, 270,
                                 c.height / 3 + 50)
            option1 = draw_table_option(screen, "Turtle", c.width / 17, c.height / 3, 270, c.height / 3 + 50)
            option3 = draw_table_option(screen, "Dragon", c.width / 17 + 270 * 2 + 70 * 2, c.height / 3, 270,
                                        c.height / 3 + 50)
            option = 2
        if option3:
            draw_selected_square(screen, "Dragon", c.width / 17 + 270 * 2 + 70 * 2, c.height / 3, 270,
                                 c.height / 3 + 50)
            option1 = draw_table_option(screen, "Turtle", c.width / 17, c.height / 3, 270, c.height / 3 + 50)
            option2 = draw_table_option(screen, "Fortress", c.width / 17 + 270 + 70, c.height / 3, 270,
                                        c.height / 3 + 50)
            option = 3
        if option == 0:
            option1 = draw_table_option(screen, "Turtle", c.width / 17, c.height / 3, 270, c.height / 3 + 50)
            option2 = draw_table_option(screen, "Fortress", c.width / 17 + 270 + 70, c.height / 3, 270,
                                        c.height / 3 + 50)
            option3 = draw_table_option(screen, "Dragon", c.width / 17 + 270 * 2 + 70 * 2, c.height / 3, 270,
                                        c.height / 3 + 50)

        start_button = utils.create_button(screen, start_button_x, start_button_y, start_button_width,
                                           start_button_height, c.light_pink, c.bright_pink)
        screen.blit(start_button_text,
                    (start_button_x + start_button_width / 6 - 2, start_button_y + start_button_height / 6))
        if start_button:
            if option != 0:
                break

        utils.quit_event()
        pygame.display.update()
