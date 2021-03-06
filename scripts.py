#!/usr/bin/env python
import math
import random
import pygame as pg
from settings import *
pg.init()


class Bubble(object):
    def __init__(self, game, x=DISPLAY_WIDTH * 0.7):
        self.color = random.choice(POSSIBLE_COLORS)
        self.border = []
        self.x = int(x)
        self.y = int(DISPLAY_HEIGHT - 50)
        self.dx = 0
        self.dy = 0
        self.radius = int(BUBBLE_SIZE / 2.)
        self.speed = BUBBLE_SPEED
        self.obj = pg.draw.circle(game.display, self.color,
                                  (self.x, self.y),
                                  self.radius)

    def handle_events(self, game, event):
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_RIGHT]:
                pass

    def update(self, game):
        print "Bubble update", self.dx, self.dy
        margin = self.radius + self.speed
        if not margin <= self.x <= DISPLAY_WIDTH - margin:
            self.dx *= -1
        if self.y <= margin:
            self.dy = 0
            self.dx = 0
            game.bubbles.some_moves = False
        self.x += int(self.dx)
        self.y += int(self.dy)
        self.x = int(self.x)
        self.y = int(self.y)
        print game.display, self.color, (self.x,  self.y),    self.radius
        self.obj = pg.draw.circle(game.display, self.color,
                                  (self.x, self.y),
                                  self.radius)
        for bubble in game.bubbles.list:
            if self.obj is bubble.obj:
                continue
            if self.obj.colliderect(bubble.obj):
                print "colidio"
                self.dx = 0
                self.dy = 0


class Bubbles(object):
    def __init__(self, game):
        self.list = []
        self.queue = []
        # self.i = 0
        self.create_a_bubble(game, DISPLAY_WIDTH * 0.5)
        self.create_a_bubble(game)
        self.some_moves = False

    def create_a_bubble(self, game, x=DISPLAY_WIDTH * 0.7):
        self.queue.append(Bubble(game, x))

    def update(self, game):
        for bubble in self.queue:
            bubble.update(game)
        for bubble in self.list:
            bubble.update(game)

    def handle_events(self, game, event):
        for bubble in self.list:
            bubble.handle_events(game, event)


class Pointer(object):
    def __init__(self, game):
        self.color = POINTER_COLOR
        self.base_x = POINTER_RATE_X * DISPLAY_WIDTH
        self.base_y = (1 - POINTER_RATE_Y) * DISPLAY_HEIGHT
        self.size = POINTER_RATE_SIZE * DISPLAY_HEIGHT
        self.x = self.base_x
        self.y = self.base_y + self.size
        self.angle = -90
        pg.draw.line(game.display, self.color,
                     (self.base_x, self.base_y), (self.x, self.y), 3)

    def throw_the_bubble(self, game):
        print "throw_the_bubble"
        game.bubbles.some_moves = True
        bubble = game.bubbles.queue[0]
        bubble.dx += bubble.speed * math.cos(math.radians(self.angle))
        bubble.dy += bubble.speed * math.sin(math.radians(self.angle))

        game.bubbles.list.append(bubble)
        game.bubbles.queue.pop(0)
        game.bubbles.queue[-1].x -= DISPLAY_WIDTH * 0.2
        game.bubbles.create_a_bubble(game)

    # def rotate(self, game, angle):
    #     print "rotate", angle, self.x, self.base_x, self.y, self.base_y
    #     self.x = self.base_x + math.cos(math.radians(angle)) * self.size
    #     self.y = self.base_y + math.sin(math.radians(angle)) * self.size

    #     pg.draw.line(game.display, self.color,
    #                      (self.base_x, self.base_y), (self.x, self.y), 3)
    #     print self.x, self.base_x, self.y, self.base_y

    def handle_events(self, game, event):
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_RIGHT]:
                self.angle += 10
            if event.key in [pg.K_LEFT]:
                self.angle += -10
            if event.key in [pg.K_RETURN, pg.K_SPACE] and not game.bubbles.some_moves:
                print "lanca a bolha"
                self.throw_the_bubble(game)
        self.angle = min(self.angle, -10)
        self.angle = max(self.angle, -170)

    def update(self, game):
        self.x = self.base_x + math.cos(math.radians(self.angle)) * self.size
        self.y = self.base_y + math.sin(math.radians(self.angle)) * self.size

        pg.draw.line(game.display, self.color,
                     (self.base_x, self.base_y), (self.x, self.y), 3)

        pg.draw.line(game.display, self.color,
                     (self.base_x, self.base_y), (self.x, self.y), 3)


class Game(object):
    def __init__(self):
        self.cmd_key_down = False
        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.pointer = Pointer(self)
        self.bubbles = Bubbles(self)
        self.loop()

    def loop(self):
        while True:
            self.display.fill((0, 0, 0))
            for event in pg.event.get():
                self.handle_common_keys(event)
                self.pointer.handle_events(self, event)
                self.bubbles.handle_events(self, event)
            self.pointer.update(self)
            self.bubbles.update(self)
            pg.display.update()
            self.clock.tick(FPS)

    def handle_common_keys(self, event):
        if event.type == pg.QUIT:
            self.quit()
        if event.type == pg.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pg.K_q:
                self.quit()
        if event.type == pg.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def quit(self):
        pg.quit()
        quit()


Game()
