#!/usr/bin/env python
import random
import pygame
pygame.init()

# SETTINGS
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
MAROON = (128,  0,   0)

# Screen
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 600


class Game(object):
    def __init__(self):
        self.cmd_key_down = False
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.loop()

    def loop(self):
        while True:
            self.display.fill((0, 0, 0))
            for event in pygame.event.get():
                self.handle_common_keys(event)
            pygame.display.update()

    def handle_common_keys(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pygame.K_q:
                self.quit()
        if event.type == pygame.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def quit(self):
        pygame.quit()
        quit()


Game()
