import pygame
import constants as c
import gui.start_window as start

pygame.init()
pygame.display.set_caption('Mahjong')
gameIcon = pygame.image.load("assets/logo.png")
pygame.display.set_icon(gameIcon)

res = (c.width, c.height)
screen = pygame.display.set_mode(res)
background = pygame.image.load("assets/background4.jpg").convert()

start.start_menu(screen, background)
