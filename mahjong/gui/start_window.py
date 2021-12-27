"""
This is the file that make the graphics the user sees when opening the app
"""
import pygame
import constants as c
import gui.utils as utils
import gui.game_window as game

pygame.init()
game_big_font = pygame.font.SysFont(c.font_type, 45, True)


def start_menu(screen, background):
    """
    This function draws the start window the player sees when they open the game.
    It also starts the music.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param background: pygame.Surface - the background image

    """
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

    turtle_img = utils.load_image("assets/Turtle.png", 270, c.height / 3 + 50)
    fortress_img = utils.load_image("assets/Fortress.png", 270, c.height / 3 + 50)
    dragon_img = utils.load_image("assets/Dragon.png", 270, c.height / 3 + 50)

    pygame.mixer.music.play(-1)
    while True:
        # create start button
        screen.blit(background, [0, 0])
        start_button = utils.create_button(screen, start_button_x, start_button_y, start_button_width,
                                           start_button_height, c.light_pink, c.bright_pink)
        # if start button was clicked draw new window that lets you choose table
        if start_button:
            table_menu(screen, background, turtle_img, fortress_img, dragon_img)
        screen.blit(start_button_text,
                    (start_button_x + start_button_width / 6 - 2, start_button_y + start_button_height / 6))

        # create quit button
        quit_button = utils.create_button(screen, quit_button_x, quit_button_y, quit_button_width,
                                          quit_button_height, c.light_pink, c.bright_pink)
        screen.blit(quit_button_text,
                    (quit_button_x + quit_button_width / 6, quit_button_y + quit_button_height / 6))

        # if quit button was clicked draw the quit window
        if quit_button:
            utils.quit_window(screen, game_big_font, c.width / 4 + 25, c.height / 4 + 25, c.width / 4 + 225,
                              c.height / 4 + 150)

        utils.quit_event()
        pygame.display.update()


def draw_table_option(screen, text, x, y, width, height, img):
    """
    Draws the image of a table option and creates
    a button with it's name that can be selected

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param text: str - the name of the table type, and the text on the button
    :param x: float/int - upper x-coordinate of table picture
    :param y: float/int - upper y-coordinate of table picture
    :param width: float/int - width of table picture
    :param height: float/int - height of table picture
    :param img: pygame.Surface - table picture
    :return: bool - True, if option button was clicked, False, if not
    """
    # draw image square
    screen.blit(img, (x, y))
    pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, width, height), 3)

    # draw button
    option_button = utils.create_button(screen, x, y + height + 20, width,
                                        50, c.light_pink, c.bright_pink)
    text_width = game_big_font.size(text)[0]
    utils.create_text(screen, game_big_font, text, c.light_blue, x + width / 2 - text_width / 2, height + 265)
    return option_button


def draw_selected_square(screen, text, x, y, width, height, img):
    """
    Draws the image of the selected table option and shows the button in a selected way

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param text: str - the name of the table type, and the text on the button
    :param x: float/int - upper x-coordinate of table picture
    :param y: float/int - upper y-coordinate of table picture
    :param width: float/int - width of table picture
    :param height: float/int - height of table picture
    :param img: pygame.Surface - table picture
    """
    # draw image square
    screen.blit(img, (x, y))
    pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, width, height), 3)

    # draw button
    pygame.draw.rect(screen, c.light_pink,
                     pygame.Rect(x, y + height + 20, width, 50))
    pygame.draw.rect(screen, c.blue, pygame.Rect(x, y + height + 20, width, 50), 3)
    text_width = game_big_font.size(text)[0]
    utils.create_text(screen, game_big_font, text, c.blue, x + width / 2 - text_width / 2, height + 265)


def table_menu(screen, background, turtle_img, fortress_img, dragon_img):
    """
    Draws the window that lets you choose which table type you want to play.
    You can't proceed without choosing

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param background: pygame.Surface - the background image
    :param turtle_img: pygame.Surface - image of the turtle table that shows an example of said table
    :param fortress_img: pygame.Surface - image of the fortress table
    :param dragon_img: pygame.Surface - image of the dragon table
    """
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

        # draw all options the same or draw the selected one as selected
        if option1:
            draw_selected_square(screen, "Turtle", c.width / 17, c.height / 3, 270, c.height / 3 + 50, turtle_img)
            option2 = draw_table_option(screen, "Fortress", c.width / 17 + 270 + 70, c.height / 3, 270,
                                        c.height / 3 + 50, fortress_img)
            option3 = draw_table_option(screen, "Dragon", c.width / 17 + 270 * 2 + 70 * 2, c.height / 3, 270,
                                        c.height / 3 + 50, dragon_img)
            option = 1

        if option2:
            draw_selected_square(screen, "Fortress", c.width / 17 + 270 + 70, c.height / 3, 270,
                                 c.height / 3 + 50, fortress_img)
            option1 = draw_table_option(screen, "Turtle", c.width / 17, c.height / 3, 270, c.height / 3 + 50,
                                        turtle_img)
            option3 = draw_table_option(screen, "Dragon", c.width / 17 + 270 * 2 + 70 * 2, c.height / 3, 270,
                                        c.height / 3 + 50, dragon_img)
            option = 2
        if option3:
            draw_selected_square(screen, "Dragon", c.width / 17 + 270 * 2 + 70 * 2, c.height / 3, 270,
                                 c.height / 3 + 50, dragon_img)
            option1 = draw_table_option(screen, "Turtle", c.width / 17, c.height / 3, 270, c.height / 3 + 50,
                                        turtle_img)
            option2 = draw_table_option(screen, "Fortress", c.width / 17 + 270 + 70, c.height / 3, 270,
                                        c.height / 3 + 50, fortress_img)
            option = 3
        if option == 0:
            option1 = draw_table_option(screen, "Turtle", c.width / 17, c.height / 3, 270, c.height / 3 + 50,
                                        turtle_img)
            option2 = draw_table_option(screen, "Fortress", c.width / 17 + 270 + 70, c.height / 3, 270,
                                        c.height / 3 + 50, fortress_img)
            option3 = draw_table_option(screen, "Dragon", c.width / 17 + 270 * 2 + 70 * 2, c.height / 3, 270,
                                        c.height / 3 + 50, dragon_img)

        # create start button
        start_button = utils.create_button(screen, start_button_x, start_button_y, start_button_width,
                                           start_button_height, c.light_pink, c.bright_pink)
        screen.blit(start_button_text,
                    (start_button_x + start_button_width / 6 - 2, start_button_y + start_button_height / 6))

        # if start button is clicked on and option is selected,
        # proceed with the game, otherwise show warning
        if start_button:
            if option != 0:
                game.init_game(screen, background, option)
            else:
                option_error(screen, c.width / 2 - 250, c.height / 2 - 150, 500, 300)

        utils.quit_event()
        pygame.display.update()


def option_error(screen, x, y, width, height):
    """
    Draws warning window that prompts player to choose a table option.

    :param screen: pygame.Surface - the screen on which the graphics will be shown
    :param x: float/int - upper x-coordinate of window
    :param y: float/int - upper y-coordinate of window
    :param width: float/int - width of window
    :param height: float/int - height of window
    :return: If ok button is click return to table_menu(screen, background, turtle_img, fortress_img, dragon_img) function
    and gives player another chance.
    """
    ok_button_text = game_big_font.render("Ok", True, c.bright_pink)
    ok_button_width = 80
    ok_button_height = 60
    ok_button_x = x + width / 2 - 30
    ok_button_y = y + height - 80

    while True:
        # draws window
        pygame.draw.rect(screen, c.bright_pink,
                         pygame.Rect(x, y, width, height))
        pygame.draw.rect(screen, c.blue, pygame.Rect(x, y, width, height), 3)

        # writes text
        text = "Please choose a table!"
        utils.create_text(screen, game_big_font, text, c.light_blue, x + 40, y + 100)

        # makes ok button
        ok_button = utils.create_button(screen, ok_button_x, ok_button_y, ok_button_width,
                                        ok_button_height, c.light_pink, c.blue)
        screen.blit(ok_button_text,
                    (ok_button_x + ok_button_width / 6 - 2, ok_button_y + ok_button_height / 6))

        if ok_button:
            return

        utils.quit_event()
        pygame.display.update()
