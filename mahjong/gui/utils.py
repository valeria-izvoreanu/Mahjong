import pygame
import constants as c
import sys


def create_button(screen, x, y, width, height, hover_color, default_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, default_color, (x, y, width, height))
    return False


def quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def create_text(screen, font, text, colour, x, y):
    txt_render = font.render(text, True, colour)
    screen.blit(txt_render, (x, y))


def convert_millis(millis):
    seconds = (millis / 1000) % 60
    minutes = (millis / (1000 * 60)) % 60
    hours = (millis / (1000 * 60 * 60)) % 24
    return seconds, minutes, hours


def quit_window(screen, font, x, y, height, width):
    yes_button_text = font.render("Yes", True, c.bright_pink)
    yes_button_width = 100
    yes_button_height = 60
    yes_button_x = width * 1.3 - yes_button_width / 2
    yes_button_y = height * 1.1 - yes_button_height * 2

    no_button_text = font.render("No", True, c.bright_pink)
    no_button_width = 100
    no_button_height = 60
    no_button_x = width * 1.95 - no_button_width / 2
    no_button_y = height * 1.1 - no_button_height * 2

    while True:
        pygame.draw.rect(screen, c.bright_pink,
                         pygame.Rect(x, y, height, width))
        pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, height, width), 3)

        text1 = font.render("Are you sure you", True, c.light_blue)
        text2 = font.render("want to quit?", True, c.light_blue)
        screen.blit(text1, (x * 1.3, y * 1.5))
        screen.blit(text2, (x * 1.45, y * 1.5 + 45))

        yes_button = create_button(screen, yes_button_x, yes_button_y, yes_button_width,
                                   yes_button_height, c.light_pink, c.blue)
        screen.blit(yes_button_text,
                    (yes_button_x + yes_button_width / 6 - 2, yes_button_y + yes_button_height / 6))
        if yes_button:
            pygame.quit()
            sys.exit()

        no_button = create_button(screen, no_button_x, no_button_y, no_button_width,
                                  no_button_height, c.light_pink, c.blue)
        screen.blit(no_button_text,
                    (no_button_x + no_button_width / 6 - 2, no_button_y + no_button_height / 6))
        if no_button:
            return True

        quit_event()
        pygame.display.update()
