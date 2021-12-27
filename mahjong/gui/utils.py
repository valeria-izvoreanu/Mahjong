import pygame
import constants as c
import sys
import gui.start_window as start


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


def load_image(address, width, height):
    icon = pygame.image.load(address).convert_alpha()
    icon = pygame.transform.scale(icon, (width, height))
    return icon


def convert_millis(millis):
    seconds = (millis / 1000) % 60
    minutes = (millis / (1000 * 60)) % 60
    hours = (millis / (1000 * 60 * 60)) % 24
    return seconds, minutes, hours


def read_table_structure(table_type):
    file1 = open('assets/' + table_type + '.txt', 'r')
    lines = file1.readlines()
    lines = [line.rstrip().split() for line in lines]
    file1.close()

    table = [[]]
    layer = 0
    for line in lines:
        if len(line) > 0:
            table[layer].append(line)
        else:
            table.append([])
            layer += 1
    return table


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


def loosing_screen(screen, background, x, y, height, width, font):
    new_button_text = font.render("New Game", True, c.bright_pink)
    new_button_width = 300
    new_button_height = 60
    new_button_x = x + 100
    new_button_y = y + 400

    no_button_text = font.render("Exit", True, c.bright_pink)
    no_button_width = 120
    no_button_height = 60
    no_button_x = x + 550
    no_button_y = y + 400

    undo_button_text = font.render("Undo last move", True, c.bright_pink)
    undo_button_width = 450
    undo_button_height = 60
    undo_button_x = x + 170
    undo_button_y = y + 300
    while True:
        pygame.draw.rect(screen, c.bright_pink,
                         pygame.Rect(x, y, height, width))
        pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, height, width), 3)

        text = "You lost!"
        create_text(screen, font, text, c.light_blue, x + width / 2 + 40, y + 80)

        text = "No more matches left!"
        text_width = font.size(text)[0]
        text_height = font.size(text)[1]
        create_text(screen, font, text, c.light_blue, x + width / 2 - text_width / 5, y + text_height + 95)

        new_button = create_button(screen, new_button_x, new_button_y, new_button_width,
                                   new_button_height, c.light_pink, c.blue)
        screen.blit(new_button_text,
                    (new_button_x + new_button_width / 6 - 2, new_button_y + new_button_height / 6))

        if new_button:
            start.start_menu(screen, background)

        no_button = create_button(screen, no_button_x, no_button_y, no_button_width,
                                  no_button_height, c.light_pink, c.blue)
        screen.blit(no_button_text,
                    (no_button_x + no_button_width / 6 - 2, no_button_y + no_button_height / 6))

        if no_button:
            pygame.quit()
            sys.exit()

        undo_button = create_button(screen, undo_button_x, undo_button_y, undo_button_width,
                                    undo_button_height, c.light_pink, c.blue)
        screen.blit(undo_button_text,
                    (undo_button_x + undo_button_width / 6 - 2, undo_button_y + undo_button_height / 6))

        if undo_button:
            return

        quit_event()
        pygame.display.update()


def winning_screen(screen, background, time_since_fst_move, table_type, x, y, height, width, font):
    new_button_text = font.render("New Game", True, c.bright_pink)
    new_button_width = 300
    new_button_height = 60
    new_button_x = x + 100
    new_button_y = y + 400

    no_button_text = font.render("Exit", True, c.bright_pink)
    no_button_width = 120
    no_button_height = 60
    no_button_x = x + 500
    no_button_y = y + 400
    while True:
        screen.blit(background, [0, 0])
        pygame.draw.rect(screen, c.bright_pink,
                         pygame.Rect(x, y, height, width))
        pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, height, width), 3)

        sec, minute, hour = convert_millis(int(time_since_fst_move))

        text = "Congratulations!"
        text_width = font.size(text)[0]
        create_text(screen, font, text, c.light_blue, x + width / 2 - text_width / 6, y + 80)

        text = "You completed the " + table_type + " table!"
        text_width = font.size(text)[0]
        text_height = font.size(text)[1]
        create_text(screen, font, text, c.light_blue, x + width / 2 - text_width / 3.5, y + text_height + 95)

        text = "Your time: " + "{hour_nr:02d}:{min_nr:02d}:{sec_nr:02d}".format(hour_nr=int(hour),
                                                                                min_nr=int(minute),
                                                                                sec_nr=int(sec))
        text_width = font.size(text)[0]
        create_text(screen, font, text, c.light_blue, x + width / 2 - text_width / 6, y + text_height * 2 + 110)

        new_button = create_button(screen, new_button_x, new_button_y, new_button_width,
                                   new_button_height, c.light_pink, c.blue)
        screen.blit(new_button_text,
                    (new_button_x + new_button_width / 6 - 2, new_button_y + new_button_height / 6))

        if new_button:
            start.start_menu(screen, background)

        no_button = create_button(screen, no_button_x, no_button_y, no_button_width,
                                  no_button_height, c.light_pink, c.blue)
        screen.blit(no_button_text,
                    (no_button_x + no_button_width / 6 - 2, no_button_y + no_button_height / 6))

        if no_button:
            pygame.quit()
            sys.exit()

        quit_event()
        pygame.display.update()
